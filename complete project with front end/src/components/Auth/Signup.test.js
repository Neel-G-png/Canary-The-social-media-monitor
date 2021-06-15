import { render, screen, fireEvent } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import Signup from './Signup';

test('renders signup page', () => {
    render(<BrowserRouter>
        <Signup />
    </BrowserRouter>);
    const input = screen.getByTestId("email")
    const inputBrand = screen.getByTestId("brand")
    const inputKeyword = screen.getByTestId("keywords")
    const inputPswd = screen.getByTestId("password")

    expect(input).toBeInTheDocument();
    expect(inputBrand).toBeInTheDocument();
    expect(inputKeyword).toBeInTheDocument();
    expect(inputPswd).toBeInTheDocument();
});

test('submit signup page form', () => {
    render(<BrowserRouter>
        <Signup />
    </BrowserRouter>);
    const input = screen.getByTestId("email")
    const inputBrand = screen.getByTestId("brand")
    const inputKeyword = screen.getByTestId("keywords")
    const inputPswd = screen.getByTestId("password")

    fireEvent.change(input, { target: { value: "riyanegi221b@gmail.com" } })
    fireEvent.change(inputPswd, { target: { value: "riyanegi" } })
    fireEvent.change(inputBrand, { target: { value: "Wired Clan" } })
    fireEvent.click(screen.getByTestId('signup'));
});

test('show required error if any field of signup form is empty', () => {
    render(<BrowserRouter>
        <Signup />
    </BrowserRouter>);
    const input = screen.getByTestId("email")
    const inputBrand = screen.getByTestId("brand")
    const inputKeyword = screen.getByTestId("keywords")
    const inputPswd = screen.getByTestId("password")
    const warning = screen.getByTestId("warning")

    fireEvent.change(input, { target: { value: "riyanegi221b@gmail.com" } })
    fireEvent.change(inputPswd, { target: { value: "riyanegi" } })
    fireEvent.change(inputBrand, { target: { value: "Wired Clan" } })
    fireEvent.click(screen.getByTestId('signup'));
    expect(warning).toBeInTheDocument()
});
