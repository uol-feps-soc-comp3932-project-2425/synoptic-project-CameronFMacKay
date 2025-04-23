import { render, screen } from "@testing-library/react";
import { vi } from "vitest";
import App from "./App.jsx";

vi.mock("./components/upload.jsx", () => ({
  default: () => <div data-testid="upload-component">Upload</div>,
}));
vi.mock("./components/lyrics.jsx", () => ({
  default: () => <div data-testid="lyrics-component">Lyrics</div>,
}));
vi.mock("./components/spotify.jsx", () => ({
  default: () => <div data-testid="spotify-component">Spotify</div>,
}));

describe("App Component", () => {
  test("renders all child components", () => {
    render(<App />);
    expect(screen.getByTestId("upload-component")).toBeInTheDocument();
    expect(screen.getByTestId("lyrics-component")).toBeInTheDocument();
    expect(screen.getByTestId("spotify-component")).toBeInTheDocument();
  });
});
