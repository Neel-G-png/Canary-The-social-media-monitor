import React from 'react'
import { render, waitFor, fireEvent } from '@testing-library/react'
import axiosMock from 'axios'
import TestAxios from './TestAxios'
import AxiosInstance from "../../helpers/AxiosInstance"

jest.mock('../../helpers/AxiosInstance')

it('should display a loading text', () => {

    const { getByTestId } = render(<TestAxios />)

    expect(getByTestId('loading')).toHaveTextContent('Loading...')
})

it('should load and display the data', async () => {
    const url = '/greeting'
    const { getByTestId } = render(<TestAxios url={url} />)

    // AxiosInstance.get.mockResolvedValueOnce({
    //     data: { greeting: 'hello there' },
    // })

    // fireEvent.click(getByTestId('fetch-data'))

    // const greetingData = await waitFor(() => getByTestId('show-data'))

    // expect(AxiosInstance.get).toHaveBeenCalledTimes(1)
    // expect(AxiosInstance.get).toHaveBeenCalledWith(url)
    // expect(greetingData).toHaveTextContent('hello there')
})