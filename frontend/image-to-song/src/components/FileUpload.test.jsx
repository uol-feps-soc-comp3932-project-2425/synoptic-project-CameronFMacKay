import { render, screen, fireEvent } from "@testing-library/react";
import FileUpload from "./upload.jsx";
import { vi } from "vitest"; // 👈 Import vitest for mocking

// 👇 Mock the unsupported browser API
global.URL.createObjectURL = vi.fn(() => "mocked-url");

describe("FileUpload Component", () => {
  test("renders input and button", () => {
    render(<FileUpload onSongDataReceived={() => {}} />);
    expect(screen.getByRole("button")).toHaveTextContent("Find Matching Songs");
    expect(screen.getByTestId("file-input")).toBeInTheDocument();
  });

  test("shows preview when a file is selected", () => {
    render(<FileUpload onSongDataReceived={() => {}} />);
    const file = new File(["dummy"], "test.jpg", { type: "image/jpeg" });
    const input = screen.getByTestId("file-input");
    fireEvent.change(input, { target: { files: [file] } });
    expect(input.files[0]).toBe(file);
  });
});
