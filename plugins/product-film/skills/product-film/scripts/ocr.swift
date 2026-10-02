// ocr.swift <png...>: prints "<file>\t<recognised text joined by |>" using macOS Vision (on-device).
// Build once: swiftc -O scripts/ocr.swift -o build/ocr
import Foundation
import Vision
import AppKit
for path in CommandLine.arguments.dropFirst() {
    guard let img = NSImage(contentsOfFile: path), let cg = img.cgImage(forProposedRect: nil, context: nil, hints: nil) else { print("\(path)\tREAD-FAIL"); continue }
    let req = VNRecognizeTextRequest(); req.recognitionLevel = .accurate; req.usesLanguageCorrection = false
    try? VNImageRequestHandler(cgImage: cg).perform([req])
    let txt = (req.results ?? []).compactMap { $0.topCandidates(1).first?.string }.joined(separator: "|")
    print("\(path)\t\(txt)")
}
