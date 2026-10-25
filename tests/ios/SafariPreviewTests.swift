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
        let field = safari.textFields["URL"].exists ? safari.textFields["URL"] : safari.textFields["Address"]
        XCTAssertTrue(field.waitForExistence(timeout: 15))
        field.tap()
        XCTAssertTrue((field.value as? String ?? "").contains("/compare/original/01/hy-alarm"))
        field.typeText("\n")
        XCTAssertTrue(safari.images.firstMatch.waitForExistence(timeout: 60), "Original iframe PDF image did not render")
        let oversized = safari.images.allElementsBoundByIndex.filter { $0.frame.width > safari.frame.width + 1 }
        XCTAssertFalse(oversized.isEmpty, "The original horizontal PDF overflow was not reproduced")
        for image in oversized { print("Original PDF image width: \(image.frame.width); iPhone viewport width: \(safari.frame.width)") }
        record("01-original-iframe-portrait")
        for _ in 0..<6 { safari.webViews.firstMatch.swipeUp(velocity: .slow) }
        record("02-original-iframe-after-scroll")
        XCUIDevice.shared.orientation = .landscapeLeft
        XCTAssertGreaterThan(safari.frame.width, safari.frame.height)
        record("03-original-iframe-landscape")
        XCUIDevice.shared.orientation = .portrait
    }
}
