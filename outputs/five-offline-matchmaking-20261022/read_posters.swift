import Foundation
import Vision
import AppKit
for path in CommandLine.arguments.dropFirst() {
    let url = URL(fileURLWithPath: path)
    guard let image = NSImage(contentsOf: url), let data = image.tiffRepresentation,
          let bitmap = NSBitmapImageRep(data: data), let cg = bitmap.cgImage else { continue }
    let request = VNRecognizeTextRequest()
    request.recognitionLevel = .accurate
    request.recognitionLanguages = ["zh-Hans", "en-US"]
    request.usesLanguageCorrection = true
    do {
        try VNImageRequestHandler(cgImage: cg).perform([request])
        let text = (request.results ?? []).compactMap { $0.topCandidates(1).first?.string }.joined(separator: "\n")
        try text.write(to: url.deletingPathExtension().appendingPathExtension("ocr.txt"), atomically: true, encoding: .utf8)
        print(url.lastPathComponent, text.count)
    } catch { print(url.lastPathComponent, error) }
}
