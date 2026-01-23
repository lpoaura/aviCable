// Snackbar message formatting helper

import type { ApiErrorResponse } from '~/types/commons';

export const generateSnackbarMessage = (response: ApiErrorResponse): string => {
    const messages: string[] = [];

    // Iterate through each key in the response object
    for (const key in response) {
        if (Object.prototype.hasOwnProperty.call(response, key)) {
            const errors = response[key];
            if (errors && errors.length > 0) {
                messages.push(...errors); // Collect all messages
            }
        }
    }

    return messages.length > 0 ? messages.join(' ') : "An unknown error occurred."; // Fallback message
}