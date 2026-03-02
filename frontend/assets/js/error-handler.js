/**
 * Centralized Error Handling Module
 * Provides consistent error processing and user feedback across the application
 * 
 * Usage:
 *   try {
 *     const data = await apiCall();
 *   } catch (error) {
 *     const displayMessage = ErrorHandler.getDisplayMessage(error);
 *     const fieldErrors = ErrorHandler.getFieldErrors(error);
 *     showError(displayMessage);
 *   }
 */

const ErrorHandler = {
    /**
     * Get user-friendly error message from API error
     * @param {Error} error - The error object
     * @returns {string} - Formatted error message for display
     */
    getDisplayMessage(error) {
        if (!error) return 'An unknown error occurred';
        
        // If it's an Error instance with message property
        if (error.message) {
            return error.message;
        }
        
        // If it's a plain object with error details
        if (error.data) {
            return error.data.detail || 
                   error.data.message || 
                   error.data.error || 
                   'Request failed';
        }
        
        // Fallback
        return String(error) || 'An unknown error occurred';
    },

    /**
     * Extract field-level validation errors
     * @param {Error} error - The error object
     * @returns {Object} - Field errors in format { fieldName: 'error message' }
     */
    getFieldErrors(error) {
        const errors = {};
        
        if (!error) return errors;
        
        // Check for errors property (our custom format)
        if (error.errors && typeof error.errors === 'object') {
            return error.errors;
        }
        
        // Check for errors in data property
        if (error.data && error.data.errors && typeof error.data.errors === 'object') {
            return error.data.errors;
        }
        
        // Check for direct field error properties
        if (error.data && typeof error.data === 'object') {
            Object.keys(error.data).forEach(key => {
                if (Array.isArray(error.data[key])) {
                    errors[key] = error.data[key][0] || 'Invalid value';
                } else if (typeof error.data[key] === 'string') {
                    errors[key] = error.data[key];
                }
            });
        }
        
        return errors;
    },

    /**
     * Format errors into a single readable string
     * @param {Error} error - The error object
     * @returns {string} - Formatted error string
     */
    formatErrorMessage(error) {
        const displayMsg = this.getDisplayMessage(error);
        const fieldErrors = this.getFieldErrors(error);
        
        if (Object.keys(fieldErrors).length === 0) {
            return displayMsg;
        }
        
        const fieldErrorsStr = Object.entries(fieldErrors)
            .map(([field, msg]) => `${field}: ${msg}`)
            .join('; ');
        
        return `${displayMsg} - ${fieldErrorsStr}`;
    },

    /**
     * Check if error is authentication-related (401)
     * @param {Error} error - The error object
     * @returns {boolean}
     */
    isAuthError(error) {
        return error && error.status === 401;
    },

    /**
     * Check if error is validation-related (400)
     * @param {Error} error - The error object
     * @returns {boolean}
     */
    isValidationError(error) {
        return error && error.status === 400;
    },

    /**
     * Check if error is not found (404)
     * @param {Error} error - The error object
     * @returns {boolean}
     */
    isNotFoundError(error) {
        return error && error.status === 404;
    },

    /**
     * Check if error is server error (500+)
     * @param {Error} error - The error object
     * @returns {boolean}
     */
    isServerError(error) {
        return error && error.status && error.status >= 500;
    },

    /**
     * Log error with context for debugging
     * @param {string} context - Where the error occurred
     * @param {Error} error - The error object
     * @param {Object} additionalData - Extra data to log
     */
    logError(context, error, additionalData = {}) {
        const logData = {
            context,
            timestamp: new Date().toISOString(),
            message: error.message || String(error),
            status: error.status,
            ...additionalData
        };
        
        if (error.data) {
            logData.data = error.data;
        }
        
        console.error('Error Log:', logData);
        
        // In production, you could send this to an error tracking service
        // Example: sendToErrorTracking(logData);
    },

    /**
     * Provides error recovery suggestions based on error type
     * @param {Error} error - The error object
     * @returns {string} - Suggested action
     */
    getSuggestion(error) {
        if (!error) return 'Please try again later';
        
        if (this.isAuthError(error)) {
            return 'Your session has expired. Please login again.';
        }
        
        if (this.isNotFoundError(error)) {
            return 'The requested resource was not found. Please refresh and try again.';
        }
        
        if (this.isServerError(error)) {
            return 'Something went wrong on our end. Please try again later.';
        }
        
        if (this.isValidationError(error)) {
            return 'Please check your input and try again.';
        }
        
        return 'Please try again or contact support if the issue persists.';
    }
};
