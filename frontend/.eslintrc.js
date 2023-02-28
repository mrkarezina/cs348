module.exports = {
  extends: ['mantine'],
  parserOptions: {
    project: './tsconfig.json',
  },
  rules: {
    'react/react-in-jsx-scope': 'off',
    'linebreak-style': 'off',
    'indent': 'off',
    'max-len': ['error', 200],
    'react/jsx-closing-tag-location': 'off',
    'react/jsx-indent-props': 'off',
    '@typescript-eslint/no-unused-vars': 'warn',
    'jsx-quotes': ['error', 'prefer-single']
  },
};
