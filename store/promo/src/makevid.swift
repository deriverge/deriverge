// Složí náhledové video z JPEG snímků a podloží ho hudbou.
// Použití: makevid <list.txt> <hudba.wav> <výstup.mp4> <šířka> <výška>
// list.txt je ve formátu ffmpeg concat: řádky "file '...'" a "duration s".
import Foundation
import AVFoundation
import CoreGraphics
import ImageIO

let args = CommandLine.arguments
guard args.count == 6, let W = Int(args[4]), let H = Int(args[5]) else {
    print("použití: makevid list.txt hudba.wav out.mp4 šířka výška"); exit(1)
}
let listPath = args[1], musicPath = args[2], outPath = args[3]

// ---- načíst seznam snímků a délek ----
var frames: [(path: String, dur: Double)] = []
let listDir = (listPath as NSString).deletingLastPathComponent
var pendingFile: String? = nil
for line in try String(contentsOfFile: listPath, encoding: .utf8).split(separator: "\n") {
    let t = line.trimmingCharacters(in: .whitespaces)
    if t.hasPrefix("file ") {
        var p = String(t.dropFirst(5)).trimmingCharacters(in: CharacterSet(charactersIn: "'\""))
        if !p.hasPrefix("/") { p = listDir + "/" + p }
        if let f = pendingFile { frames.append((f, 0.5)) }   // předchozí bez duration
        pendingFile = p
    } else if t.hasPrefix("duration ") {
        if let f = pendingFile, let d = Double(t.dropFirst(9)) {
            frames.append((f, max(0.02, d))); pendingFile = nil
        }
    }
}
if let f = pendingFile { frames.append((f, 0.5)) }
guard frames.count > 5 else { print("málo snímků"); exit(1) }
let total = frames.reduce(0.0) { $0 + $1.dur }
print("snímků \(frames.count), délka \(String(format: "%.1f", total)) s")

func loadCG(_ path: String) -> CGImage? {
    guard let src = CGImageSourceCreateWithURL(URL(fileURLWithPath: path) as CFURL, nil) else { return nil }
    return CGImageSourceCreateImageAtIndex(src, 0, nil)
}

// ---- 1) video bez zvuku ----
let tmpVideo = outPath + ".video.mp4"
try? FileManager.default.removeItem(atPath: tmpVideo)
let writer = try AVAssetWriter(outputURL: URL(fileURLWithPath: tmpVideo), fileType: .mp4)
let vSettings: [String: Any] = [
    AVVideoCodecKey: AVVideoCodecType.h264,
    AVVideoWidthKey: W, AVVideoHeightKey: H,
    AVVideoCompressionPropertiesKey: [
        AVVideoAverageBitRateKey: 9_000_000,
        AVVideoProfileLevelKey: AVVideoProfileLevelH264HighAutoLevel,
        AVVideoMaxKeyFrameIntervalKey: 60,
    ],
]
let vin = AVAssetWriterInput(mediaType: .video, outputSettings: vSettings)
vin.expectsMediaDataInRealTime = false
let adaptor = AVAssetWriterInputPixelBufferAdaptor(assetWriterInput: vin, sourcePixelBufferAttributes: [
    kCVPixelBufferPixelFormatTypeKey as String: kCVPixelFormatType_32BGRA,
    kCVPixelBufferWidthKey as String: W, kCVPixelBufferHeightKey as String: H,
])
writer.add(vin)
writer.startWriting()
writer.startSession(atSourceTime: .zero)

func pixelBuffer(from cg: CGImage) -> CVPixelBuffer? {
    var pb: CVPixelBuffer?
    guard adaptor.pixelBufferPool != nil,
          CVPixelBufferPoolCreatePixelBuffer(nil, adaptor.pixelBufferPool!, &pb) == kCVReturnSuccess,
          let buf = pb else { return nil }
    CVPixelBufferLockBaseAddress(buf, [])
    defer { CVPixelBufferUnlockBaseAddress(buf, []) }
    guard let ctx = CGContext(data: CVPixelBufferGetBaseAddress(buf),
                              width: W, height: H,
                              bitsPerComponent: 8,
                              bytesPerRow: CVPixelBufferGetBytesPerRow(buf),
                              space: CGColorSpaceCreateDeviceRGB(),
                              bitmapInfo: CGImageAlphaInfo.premultipliedFirst.rawValue |
                                          CGBitmapInfo.byteOrder32Little.rawValue) else { return nil }
    ctx.interpolationQuality = .high
    ctx.draw(cg, in: CGRect(x: 0, y: 0, width: W, height: H))
    return buf
}

// Konstantních 30 fps: řídké zdrojové snímky se opakují na každém ticku.
// Proměnlivá frekvence s dlouhými mezerami Applu vadí
// (chyba MOV_RESAVE_FRAME_RATE_LARGER při zpracování náhledu).
let SCALE = CMTimeScale(600)
let FPS = 30.0
let tick = CMTime(value: CMTimeValue(600.0 / FPS), timescale: SCALE)
var starts: [Double] = []
var acc = 0.0
for fr in frames { starts.append(acc); acc += fr.dur }
let totalTicks = Int((acc * FPS).rounded(.down))

var srcIx = -1
var buf: CVPixelBuffer? = nil
var pts = CMTime.zero
for t in 0..<totalTicks {
    let now = Double(t) / FPS
    while srcIx + 1 < frames.count && starts[srcIx + 1] <= now + 0.0001 {
        srcIx += 1
        if let cg = loadCG(frames[srcIx].path) { buf = pixelBuffer(from: cg) }
    }
    guard let b = buf else { continue }
    while !vin.isReadyForMoreMediaData { Thread.sleep(forTimeInterval: 0.005) }
    adaptor.append(b, withPresentationTime: pts)
    pts = CMTimeAdd(pts, tick)
    if t % 120 == 0 { print("  tick \(t)/\(totalTicks)") }
}
vin.markAsFinished()
writer.endSession(atSourceTime: pts)
let sem = DispatchSemaphore(value: 0)
writer.finishWriting { sem.signal() }
sem.wait()
guard writer.status == .completed else { print("zápis videa selhal: \(String(describing: writer.error))"); exit(1) }
print("video hotové")

// ---- 2) přidat hudbu s náběhem a dozněním ----
let comp = AVMutableComposition()
let videoAsset = AVURLAsset(url: URL(fileURLWithPath: tmpVideo))
let musicAsset = AVURLAsset(url: URL(fileURLWithPath: musicPath))
guard let vTrackSrc = videoAsset.tracks(withMediaType: .video).first,
      let aTrackSrc = musicAsset.tracks(withMediaType: .audio).first,
      let vTrack = comp.addMutableTrack(withMediaType: .video, preferredTrackID: kCMPersistentTrackID_Invalid),
      let aTrack = comp.addMutableTrack(withMediaType: .audio, preferredTrackID: kCMPersistentTrackID_Invalid) else {
    print("stopy se nepodařilo připravit"); exit(1)
}
let vDur = videoAsset.duration
try vTrack.insertTimeRange(CMTimeRange(start: .zero, duration: vDur), of: vTrackSrc, at: .zero)
let aDur = min(vDur, musicAsset.duration)
try aTrack.insertTimeRange(CMTimeRange(start: .zero, duration: aDur), of: aTrackSrc, at: .zero)

let mix = AVMutableAudioMix()
let par = AVMutableAudioMixInputParameters(track: aTrack)
let base: Float = 0.55
par.setVolumeRamp(fromStartVolume: 0, toEndVolume: base,
                  timeRange: CMTimeRange(start: .zero, duration: CMTime(seconds: 1, preferredTimescale: SCALE)))
let fadeStart = CMTimeSubtract(vDur, CMTime(seconds: 2, preferredTimescale: SCALE))
par.setVolumeRamp(fromStartVolume: base, toEndVolume: 0,
                  timeRange: CMTimeRange(start: fadeStart, duration: CMTime(seconds: 2, preferredTimescale: SCALE)))
mix.inputParameters = [par]

try? FileManager.default.removeItem(atPath: outPath)
guard let exp = AVAssetExportSession(asset: comp, presetName: AVAssetExportPresetHighestQuality) else {
    print("export se nepodařilo založit"); exit(1)
}
exp.outputURL = URL(fileURLWithPath: outPath)
exp.outputFileType = .mp4
exp.audioMix = mix
let sem2 = DispatchSemaphore(value: 0)
exp.exportAsynchronously { sem2.signal() }
sem2.wait()
guard exp.status == .completed else { print("export selhal: \(String(describing: exp.error))"); exit(1) }
try? FileManager.default.removeItem(atPath: tmpVideo)
print("HOTOVO \(outPath)")
