import { render, screen } from "@testing-library/react";
import Lyrics from "./lyrics.jsx";

describe("Lyrics Component", () => {
  test("shows message when no songData is present", () => {
    render(<Lyrics songData={null} />);
    expect(
      screen.getByText(/Upload an image to see matching lyrics/i)
    ).toBeInTheDocument();
  });

  test("displays song info when songData is provided", () => {
    const mockData = {
      tag: [
        {
          artist: "Test Artist",
          title: "Test Song",
          overall_similarity: 0.85,
          lyrics: [{ text: "This is a line", words: [] }],
        },
      ],
      image: "beach",
      brightness: 200,
      contrast: 50,
      main_colour: [123, 45, 67],
    };

    render(<Lyrics songData={mockData} />);

    // Use getByRole to specifically target the heading
    expect(
      screen.getByRole("heading", { name: /Test Song/i })
    ).toBeInTheDocument();

    // Match the text that includes the artist, scoped with getByText
    expect(screen.getByText(/by\s+Test Artist/i)).toBeInTheDocument();

    // Optional: Confirm the line is rendered
    expect(screen.getByText(/This is a line/i)).toBeInTheDocument();
  });
});
