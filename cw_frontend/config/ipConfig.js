const config = {
  isDevelopment: process.env.NODE_ENV === 'production', // Add this line
  developmentServerIP: 'http://127.0.0.1',
  productionServerIP: 'http://192.168.20.195',
};

export default config;
