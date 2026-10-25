import XCTest

final class SafariPreviewTests: XCTestCase {
    let safari = XCUIApplication(bundleIdentifier: "com.apple.mobilesafari")

    func record(_ name: String) {
        let tree = XCTAttachment(string: safari.debugDescription)
        tree.name = name + "-accessibility"
        tree.lifetime = .keepAlways
        add(tree)
        let picture = XCTAttachment(screenshot: XCUIScreen.main.screenshot())
        picture.name = name
        picture.lifetime = .keepAlways
        add(picture)
    }

    func testOriginalIframePresentation() {
        continueAfterFailure = false
        XCUIDevice.shared.orientation = .portrait
        safari.launch()
        for _ in 0..<3 {
            let button = safari.buttons["Continue"]
            if button.waitForExistence(timeout: 2) { button.tap() }
        }
        let original = safari.otherElements["PDF Viewer"].firstMatch
        XCTAssertTrue(original.waitForExistence(timeout: 60), "Original HTML document did not load")
        let pdfImage = original.images.firstMatch
        XCTAssertTrue(pdfImage.waitForExistence(timeout: 30), "Original iframe PDF image did not render")
        record("01-original-iframe-portrait")
        let imageWidth = pdfImage.frame.width
        let viewportWidth = safari.frame.width
        print("Original PDF image width: \(imageWidth); iPhone viewport width: \(viewportWidth)")
        XCTAssertGreaterThan(imageWidth, viewportWidth + 1, "Original horizontal overflow was not reproduced")
        for _ in 0..<6 { safari.webViews.firstMatch.swipeUp(velocity: .slow) }
        record("02-original-iframe-after-scroll")
        XCUIDevice.shared.orientation = .landscapeLeft
        XCTAssertGreaterThan(safari.frame.width, safari.frame.height)
        record("03-original-iframe-landscape")
        XCUIDevice.shared.orientation = .portrait
    }
}
