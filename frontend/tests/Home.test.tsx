import { render, screen } from '@testing-library/react';
import Home from '../src/app/page'; // Adjust path if necessary

describe('Home', () => {
  it('renders a heading', () => {
    render(<Home />);
    const heading = screen.getByRole('heading', { name: /Local Voice Assistant/i });
    expect(heading).toBeInTheDocument();
  });
});
