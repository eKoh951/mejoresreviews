import { createFileRoute } from "@tanstack/react-router";
import { Star, QrCode, BarChart3, MessageSquare, MapPin, ShieldCheck, Zap } from "lucide-react";
import { Button } from "@/components/ui/button";

export const Route = createFileRoute("/como-funciona")({
  component: ComoFunciona,
});

const useCases = [
  {
    icon: QrCode,
    title: "Solicitud de reseña con QR o enlace",
    desc: "Genera un código QR o enlace directo que lleva a tus clientes directamente a la página de reseñas de tu negocio en Google. Ponlo en tu menú, recibo, vitrina o envíalo por WhatsApp.",
  },
  {
    icon: MessageSquare,
    title: "Plantillas de respuesta",
    desc: "Responde reseñas positivas y negativas con plantillas profesionales adaptadas al tono de tu negocio. Recuperar a un cliente insatisfecho puede convertirse en tu mejor reseña.",
  },
  {
    icon: BarChart3,
    title: "Panel de seguimiento",
    desc: "Monitorea el crecimiento de tus reseñas, tu calificación promedio y compara tu desempeño frente a competidores locales — todo en un solo lugar.",
  },
  {
    icon: MapPin,
    title: "Optimización para Google Maps",
    desc: "Te mostramos qué keywords buscan tus clientes en tu zona y cómo optimizar tu perfil de Google Business para aparecer primero.",
  },
  {
    icon: ShieldCheck,
    title: "Monitoreo de reseñas falsas",
    desc: "Detectamos reseñas sospechosas y te guiamos para reportarlas correctamente a Google — sin represalias, sin riesgo para tu cuenta.",
  },
  {
    icon: Zap,
    title: "Alertas en tiempo real",
    desc: "Recibe una notificación cada vez que alguien deja una reseña para que puedas responder rápido — la velocidad de respuesta también mejora tu posicionamiento.",
  },
];

function ComoFunciona() {
  return (
    <div className="mx-auto max-w-6xl px-4 sm:px-6 py-16">
      <div className="text-center mb-16">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-[hsl(var(--primary))/10] text-[hsl(var(--primary))] text-sm font-medium mb-4">
          <Star className="h-3.5 w-3.5 fill-current" />
          Simple, honesto, efectivo
        </div>
        <h1 className="text-4xl md:text-5xl font-bold mb-4">Cómo funciona MejoresReseñas</h1>
        <p className="text-[hsl(var(--muted-foreground))] max-w-2xl mx-auto text-lg">
          Una plataforma diseñada para que cualquier negocio — aunque no seas experto en tecnología — pueda conseguir más reseñas auténticas y crecer en Google.
        </p>
      </div>

      {/* Step-by-step */}
      <div className="mb-20 space-y-12">
        {[
          {
            n: "1",
            title: "Conecta tu Perfil de Google Business",
            desc: "Vincula tu Perfil de Negocio de Google en menos de 5 minutos. No necesitas darnos acceso a tu cuenta de Google Ads ni a tus campañas. Solo necesitamos leer tu información pública de negocio.",
            note: "Usamos OAuth 2.0 de Google. Tú controlas qué permisos otorgas y puedes revocarlos en cualquier momento.",
          },
          {
            n: "2",
            title: "Crea tu enlace o QR de solicitud",
            desc: "Genera un enlace personalizado o código QR que lleva a tus clientes directo a tu página de reseñas de Google. Sin pasos extra, sin crear cuentas — tus clientes solo escanean y escriben.",
            note: "El enlace funciona desde cualquier celular con Android o iPhone, con o sin la app de Google Maps instalada.",
          },
          {
            n: "3",
            title: "Pide reseñas en el momento correcto",
            desc: "El mejor momento para pedir una reseña es justo después de una buena experiencia. Te ayudamos con scripts de conversación, mensajes de WhatsApp y señalética para tu local.",
            note: "Nunca ofrecemos incentivos a cambio de reseñas — eso viola las políticas de Google y puede costarle la cuenta a tu negocio.",
          },
          {
            n: "4",
            title: "Responde y gestiona todas tus reseñas",
            desc: "Responder a todas las reseñas — positivas y negativas — es uno de los factores de posicionamiento más importantes en Google Maps. Te lo hacemos fácil con plantillas y sugerencias inteligentes.",
            note: "Las respuestas profesionales a reseñas negativas le muestran a clientes potenciales que te importa el servicio.",
          },
        ].map((step) => (
          <div key={step.n} className="flex flex-col md:flex-row gap-6 items-start">
            <div className="flex-shrink-0 h-12 w-12 rounded-full bg-[hsl(var(--primary))] text-[hsl(var(--primary-foreground))] flex items-center justify-center text-lg font-bold">
              {step.n}
            </div>
            <div>
              <h2 className="text-xl font-bold mb-2">{step.title}</h2>
              <p className="text-[hsl(var(--muted-foreground))] mb-2">{step.desc}</p>
              <p className="text-xs text-[hsl(var(--muted-foreground))] bg-[hsl(var(--muted))] rounded-lg px-3 py-2 border-l-2 border-[hsl(var(--primary))]">
                💡 {step.note}
              </p>
            </div>
          </div>
        ))}
      </div>

      {/* Features grid */}
      <h2 className="text-2xl font-bold text-center mb-10">Todo lo que incluye la plataforma</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-16">
        {useCases.map((u) => (
          <div key={u.title} className="rounded-xl border border-[hsl(var(--border))] p-6 bg-[hsl(var(--card))]">
            <div className="h-10 w-10 rounded-lg bg-[hsl(var(--primary))/10] flex items-center justify-center mb-4">
              <u.icon className="h-5 w-5 text-[hsl(var(--primary))]" />
            </div>
            <h3 className="font-semibold mb-2">{u.title}</h3>
            <p className="text-sm text-[hsl(var(--muted-foreground))] leading-relaxed">{u.desc}</p>
          </div>
        ))}
      </div>

      <div className="text-center">
        <Button size="lg">Comenzar gratis ahora</Button>
        <p className="text-xs text-[hsl(var(--muted-foreground))] mt-3">Sin tarjeta de crédito. Sin contratos. Cancela cuando quieras.</p>
      </div>
    </div>
  );
}
