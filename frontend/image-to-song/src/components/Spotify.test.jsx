import { render, screen } from "@testing-library/react";
import Spotify from "./spotify.jsx";

describe("Spotify Component", () => {
  test("renders placeholder when no songData is provided", () => {
    render(<Spotify songData={null} />);
    expect(
      screen.getByText(/Upload an image to see matching songs/i)
    ).toBeInTheDocument();
  });

  test("renders artist and title when songData exists", () => {
    const mockData = {
      tag: [
        {
          artist: "Artist A",
          title: "Song A",
          overall_similarity: 0.95,
        },
      ],
    };

    render(<Spotify songData={mockData} />);

    // Match song title heading
    expect(
      screen.getByRole("heading", { name: /Song A/i })
    ).toBeInTheDocument();

    // Match artist line
    expect(screen.getByText(/by\s+Artist A/i)).toBeInTheDocument();

    // Optionally: check dropdown option
    expect(
      screen.getByRole("option", { name: /Artist A - Song A/i })
    ).toBeInTheDocument();
  });
});
