import "./globals.css";

export const metadata = {
  title: "Grand Line | One Piece",
  description: "Un homenaje interactivo a One Piece — tripulación, frutas del diablo, sagas, recompensas y más.",
  icons: {
    // URL-encodado (%3C = <, %3E = >) para ser un data URI válido según el validador W3C
    icon: "data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%20100%20100'%3E%3Ctext%20y='.9em'%20font-size='90'%3E%F0%9F%8F%B4%E2%80%8D%E2%98%A0%EF%B8%8F%3C/text%3E%3C/svg%3E",
  },
};

export default function RootLayout({ children }) {
  return (
    <html lang="es">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link
          href="https://fonts.googleapis.com/css2?family=Pirata+One&family=Cinzel:wght@500;700;900&family=Crimson+Text:ital,wght@0,400;0,600;1,400&display=swap"
          rel="stylesheet"
        />
      </head>
      <body>{children}</body>
    </html>
  );
}
