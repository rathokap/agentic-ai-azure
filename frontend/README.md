# Customer Support Agent - Frontend

A modern, responsive React-based frontend for the AI-powered Customer Support Agent. Built with React, TypeScript, and Vite.

## Features

- 🎨 **Modern UI**: Beautiful gradient design with smooth animations
- 💬 **Conversational Interface**: Chat-like interface for natural interactions
- 📱 **Responsive Design**: Works seamlessly on desktop, tablet, and mobile
- 🌓 **Dark Mode Support**: Automatically adapts to system preferences
- ⚡ **Fast & Lightweight**: Built with Vite for optimal performance
- 🔄 **Real-time Updates**: Instant message updates with loading indicators

## Prerequisites

- Node.js (v18 or higher)
- npm or yarn package manager
- Backend API running (see `../backend/README.md`)

## Installation

1. **Navigate to the frontend directory:**
   ```powershell
   cd frontend
   ```

2. **Install dependencies:**
   ```powershell
   npm install
   ```

## Configuration

The frontend uses environment variables for configuration. Create or modify the `.env` file:

```env
VITE_API_URL=http://localhost:8000
```

- `VITE_API_URL`: The URL of your backend API (default: `http://localhost:8000`)

## Running the Application

### Development Mode

Start the development server with hot-reload:

```powershell
npm run dev
```

The application will be available at `http://localhost:3000`

### Production Build

Build the application for production:

```powershell
npm run build
```

Preview the production build:

```powershell
npm run preview
```

## Usage

1. **Start the Backend**: Make sure your backend API is running on port 8000
   ```powershell
   cd ../backend
   python app.py
   ```

2. **Start the Frontend**: In a new terminal, start the frontend
   ```powershell
   cd frontend
   npm run dev
   ```

3. **Open Browser**: Navigate to `http://localhost:3000`

4. **Start Chatting**: Type your questions in the input field and press Enter or click the send button

## Project Structure

```
frontend/
├── src/
│   ├── components/         # React components
│   │   ├── ChatMessage.tsx    # Message bubble component
│   │   ├── ChatMessage.css
│   │   ├── ChatInput.tsx      # Input field component
│   │   └── ChatInput.css
│   ├── services/          # API services
│   │   └── api.ts            # Backend API integration
│   ├── App.tsx            # Main application component
│   ├── App.css            # Main application styles
│   ├── main.tsx           # Application entry point
│   ├── index.css          # Global styles
│   └── vite-env.d.ts      # TypeScript declarations
├── index.html             # HTML template
├── package.json           # Dependencies and scripts
├── tsconfig.json          # TypeScript configuration
├── vite.config.ts         # Vite configuration
└── .env                   # Environment variables
```

## API Integration

The frontend communicates with the backend via REST API:

### Endpoint: POST `/support-agent`

**Parameters:**
- `query` (string): User's question or message
- `uid` (string): Unique user session identifier

**Response:**
```json
{
  "result": "Agent's response message"
}
```

## Customization

### Changing Colors

Edit the gradient colors in `src/App.css`:

```css
.app {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
```

### Modifying the UI

- **Header**: Edit the `app-header` section in `src/App.tsx`
- **Messages**: Modify `src/components/ChatMessage.tsx` and its CSS
- **Input**: Customize `src/components/ChatInput.tsx` and its CSS

### Backend URL

To connect to a different backend URL:

1. Update `.env` file:
   ```env
   VITE_API_URL=https://your-api-url.com
   ```

2. Restart the development server

## Troubleshooting

### Backend Connection Issues

**Error**: "Failed to get response from support agent"

**Solutions:**
1. Ensure backend is running on the correct port
2. Check CORS configuration in backend `app.py`
3. Verify `VITE_API_URL` in `.env` matches backend URL

### Port Already in Use

If port 3000 is already in use, modify `vite.config.ts`:

```typescript
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3001,  // Change to desired port
    host: true
  }
})
```

### TypeScript Errors

Run type checking:
```powershell
npm run lint
```

## Deployment

### Azure Static Web Apps

1. Build the application:
   ```powershell
   npm run build
   ```

2. Deploy the `dist` folder to Azure Static Web Apps

3. Update environment variables in Azure portal

### Docker

Create a `Dockerfile`:

```dockerfile
FROM node:18-alpine as build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

Build and run:
```powershell
docker build -t support-agent-frontend .
docker run -p 80:80 support-agent-frontend
```

## Technologies Used

- **React 18**: UI library
- **TypeScript**: Type-safe JavaScript
- **Vite**: Build tool and dev server
- **Axios**: HTTP client for API calls
- **CSS3**: Styling with modern features

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - See LICENSE file for details

## Support

For issues or questions:
- Check the troubleshooting section
- Review backend logs
- Open an issue in the repository

---

**Note**: This frontend is designed to work with the agentic-ai backend. Make sure the backend is properly configured and running before using the frontend.
