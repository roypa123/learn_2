#include <iostream>
#include <string>
#include "font.h"
#include "deflate.h"

void printGlyph(char c) {
    std::cout << "'" << c << "':";
    for (int y = 0; y < kGlyphHeight; ++y) {
        std::cout << " " << hexByte(kFont[glyphIndex(c)][y]);
    }
    std::cout << "\n";
    for (int y = 0; y < kGlyphHeight; ++y) {
        std::cout << "    ";
        for (int x = 0; x < kGlyphWidth; ++x) {
            std::cout << (glyphPixel(c, x, y) ? '#' : '.');
        }
        std::cout << "\n";
    }
}

void printText(const std::string& text) {
    Image picture(textWidth(text, 1), textHeight(text, 1), colours::white);
    drawText(picture, 0, 0, text, colours::black);
    for (int y = 0; y < picture.height(); ++y) {
        for (int x = 0; x < picture.width(); ++x) {
            std::cout << (picture.getPixel(x, y).r == 0 ? '#' : ' ');
        }
        std::cout << "\n";
    }
}

int countDark(const Image& picture) {
    int count = 0;
    for (int y = 0; y < picture.height(); ++y) {
        for (int x = 0; x < picture.width(); ++x) {
            count += (picture.getPixel(x, y).r < 128) ? 1 : 0;
        }
    }
    return count;
}

int main() {
    printGlyph('A');
    printGlyph('g');
    printText("Hello, world!");

    const std::string two = "Line one\nand two";
    std::cout << "\"Hello, world!\": " << textWidth("Hello, world!", 1) << " x "
              << textHeight("Hello, world!", 1) << " pixels; at scale 3: "
              << textWidth("Hello, world!", 3) << " x " << textHeight("Hello, world!", 3) << "\n";
    std::cout << "two lines: " << lineCount(two) << " lines, " << textWidth(two, 1) << " x "
              << textHeight(two, 1) << " pixels\n";
    std::cout << "a character outside the font is drawn as '?': glyph " << glyphIndex('\t')
              << " = glyph " << glyphIndex('?') << "\n";

    std::cout << "'I' at (0.3, 0.0), size 2.5: coverage of pixel (2, 0) = "
              << glyphCoverage('I', 0.3, 0.0, 2.5, 2, 0) << ", of pixel (2, 2) = "
              << glyphCoverage('I', 0.3, 0.0, 2.5, 2, 2) << ", of pixel (3, 0) = "
              << glyphCoverage('I', 0.3, 0.0, 2.5, 3, 0) << "\n";

    Image sheet(16 * kCharAdvance * 3 + 12, 6 * kLineAdvance * 3 + 12, colours::white);
    for (int code = kFirstChar; code <= kLastChar; ++code) {
        const int i = code - kFirstChar;
        drawText(sheet, 6 + (i % 16) * kCharAdvance * 3, 6 + (i / 16) * kLineAdvance * 3,
                 std::string(1, static_cast<char>(code)), colours::black, 3);
    }
    std::cout << "font sheet: " << sheet.width() << " x " << sheet.height() << ", "
              << countDark(sheet) << " dark pixels\n";

    Image sizes(300, 125, colours::white);
    const double steps[5] = {1.0, 1.5, 2.0, 3.0, 4.5};
    double y = 6.0;
    for (double s : steps) {
        drawTextSmooth(sizes, 6.0, y, "Smooth " + std::to_string(s).substr(0, 3), colours::black, s);
        y += kLineAdvance * s;
    }

    Image label(300, 200);
    for (int py = 0; py < 200; ++py) {
        const Colour c = lerpColour(Colour{40, 90, 200}, Colour{250, 200, 120}, py / 199.0);
        for (int px = 0; px < 300; ++px) {
            label.setPixel(px, py, c);
        }
    }
    const std::string title = "Evening sky";
    drawTextCentred(label, 152, 22, title, Colour{20, 30, 60}, 4);
    drawTextCentred(label, 150, 20, title, colours::white, 4);
    const std::string caption = "300 x 200 pixels\nsaved as a PNG";
    const Rect box = textBox(20, 150, caption, 2, 6);
    fillRectAlpha(label, box, colours::black, 0.5);
    drawText(label, 20, 150, caption, colours::white, 2);
    std::cout << "caption box: " << box.x0 << ", " << box.y0 << " to " << box.x1 << ", " << box.y1
              << "\n";

    if (!savePNGCompressed(sheet, "font.png") || !savePNGCompressed(sizes, "sizes.png") ||
        !savePNGCompressed(label, "label.png")) {
        std::cout << "could not write the files\n";
        return 1;
    }
    std::cout << "wrote font.png, sizes.png and label.png\n";
    return 0;
}
