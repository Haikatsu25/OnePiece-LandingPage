import { Pirata_One, Cinzel, Crimson_Text } from "next/font/google";
import "./globals.css";

// next/font: fuentes auto-hospedadas por Next.js, sin <link> externo y sin salto de layout
const pirata = Pirata_One({ weight: "400", subsets: ["latin"], variable: "--font-pirata", display: "swap" });
const cinzel = Cinzel({ weight: ["500", "700", "900"], subsets: ["latin"], variable: "--font-cinzel", display: "swap" });
const crimson = Crimson_Text({ weight: ["400", "600"], style: ["normal", "italic"], subsets: ["latin"], variable: "--font-crimson", display: "swap" });

const TITULO = "Grand Line | One Piece";
const DESCRIPCION = "Un homenaje interactivo a One Piece — tripulación, frutas del diablo, sagas, galería, tráilers oficiales y un chat con IA.";

export const metadata = {
  metadataBase: new URL("https://one-piece-landing-page-six.vercel.app"),
  title: TITULO,
  description: DESCRIPCION,
  icons: {
    // URL-encodado (%3C = <, %3E = >, %20 = espacio) para ser un data URI válido según el validador W3C
    icon: "data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%20100%20100'%3E%3Ctext%20y='.9em'%20font-size='90'%3E%F0%9F%8F%B4%E2%80%8D%E2%98%A0%EF%B8%8F%3C/text%3E%3C/svg%3E",
  },
  openGraph: {
    title: TITULO,
    description: DESCRIPCION,
    url: "/",
    siteName: "Grand Line",
    locale: "es_MX",
    type: "website",
    images: [{ url: "/img/gear5-toei.jpg", width: 960, height: 540, alt: "Luffy en Gear 5" }],
  },
  twitter: { card: "summary_large_image", title: TITULO, description: DESCRIPCION, images: ["/img/gear5-toei.jpg"] },
};

export default function RootLayout({ children }) {
  return (
    <html lang="es" className={`${pirata.variable} ${cinzel.variable} ${crimson.variable}`}>
      <body>{children}</body>
    </html>
  );
}
