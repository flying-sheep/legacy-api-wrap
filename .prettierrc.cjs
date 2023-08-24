module.exports = {
    plugins: [require.resolve('prettier-plugin-jinja-template')],
    overrides: [
        {
            files: ['.vscode/*.json'],
            options:{
                parser: 'json5',
                quoteProps: 'preserve',
                singleQuote: false,
                trailingComma: 'all',
            },
        },
        {
            files: ["*.html"],
            options: {
                parser: 'jinja-template',
            },
        },
    ]
}
