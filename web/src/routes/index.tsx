import { createFileRoute, Link } from "@tanstack/react-router";
import { Star, MapPin, MessageSquare, TrendingUp, QrCode, ShieldCheck, ChevronRight, CheckCircle } from "lucide-react";
import { Button } from "@/components/ui/button";

export const Route = createFileRoute("/")({
  component: Home,
});

function StarRating({ n = 5 }: { n?: number }) {
  return (
    <span className="flex gap-0.5">
      {Array.from({ length: n }).map((_, i) => (
        <Star key={i} className="h-4 w-4 fill-[hsl(var(--accent))] text-[hsl(var(--accent))]" />
      ))}
    </span>
  );
}

const features = [
  {
    icon: Star,
    title: "Más reseñas auténticas",
    desc: "Te damos las herramientas para pedirle reseñas a tus clientes de forma natural, sin violar las políticas de Google.",
  },
  {
    icon: MapPin,
    title: "Mayor visibilidad en Maps",
    desc: "Más reseñas = mejor posicionamiento en Google Maps. Aparece primero cuando tus clientes buscan lo que vendes.",
  },
  {
    icon: MessageSquare,
    title: "Responde como un profesional",
    desc: "Plantillas y guías para responder reseñas negativas de manera que recuperes al cliente y construyas confianza.",
  },
  {
    icon: QrCode,
    title: "Solicitud con código QR",
    desc: "Genera un código QR o enlace directo para que tus clientes dejen su reseña en segundos desde su celular.",
  },
  {
    icon: TrendingUp,
    title: "Análisis de keywords locales",
    desc: "Descubre exactamente cómo buscan tus clientes en Ciudad Juárez y Chihuahua para que aparezcas antes que tu competencia.",
  },
  {
    icon: ShieldCheck,
    title: "100% conforme con Google",
    desc: "Nunca compramos reseñas, nunca creamos reseñas falsas. Todo lo que hacemos está dentro de las políticas de Google.",
  },
];

const steps = [
  { n: "01", title: "Conecta tu negocio", desc: "Vincula tu perfil de Google Business en minutos. Sin tarjeta de crédito requerida." },
  { n: "02", title: "Invita a tus clientes", desc: "Usa tu link o QR personalizado para solicitar reseñas justo después de la visita o compra." },
  { n: "03", title: "Crece tu reputación", desc: "Monitorea tus reseñas, responde fácilmente y mira cómo sube tu calificación semana a semana." },
];

const testimonials = [
  { name: "Ana G.", biz: "Restaurante El Mezquite, Juárez", stars: 5, quote: "Pasamos de 14 reseñas a 87 en dos meses. Ahora somos el restaurante mejor calificado de nuestra zona." },
  { name: "Carlos M.", biz: "Taller Mecánico Monterrey, Chihuahua", stars: 5, quote: "Mis clientes antes no dejaban reseñas. Con el QR empezaron a hacerlo solos. Súper fácil." },
  { name: "María L.", biz: "Salón de Belleza Style, Juárez", stars: 5, quote: "Google me encuentra ahora. Tengo más citas nuevas cada semana solo por las reseñas." },
];

function Home() {
  return (
    <>
      {/* Hero */}
      <section className="relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-[hsl(var(--primary))/5] to-[hsl(var(--accent))/5] pointer-events-none" />
        <div className="mx-auto max-w-6xl px-4 sm:px-6 py-24 md:py-36 text-center relative">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-[hsl(var(--primary))/10] text-[hsl(var(--primary))] text-sm font-medium mb-6">
            <Star className="h-3.5 w-3.5 fill-current" />
            Para negocios en México — 100% conforme con Google
          </div>
          <h1 className="text-4xl md:text-6xl font-bold tracking-tight text-[hsl(var(--foreground))] mb-6 leading-tight">
            Más reseñas reales.<br />
            <span className="text-[hsl(var(--primary))]">Más clientes.</span><br />
            Más ventas.
          </h1>
          <p className="text-lg md:text-xl text-[hsl(var(--muted-foreground))] max-w-2xl mx-auto mb-10">
            Ayudamos a restaurantes y negocios locales en Ciudad Juárez y Chihuahua a conseguir más reseñas auténticas en Google, mejorar su posición en Maps y crecer su reputación online — sin trucos, sin comprar reseñas.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button size="lg" className="gap-2">
              Comenzar gratis <ChevronRight className="h-4 w-4" />
            </Button>
            <Button size="lg" variant="outline" asChild>
              <Link to="/como-funciona">Cómo funciona</Link>
            </Button>
          </div>
          <div className="mt-12 flex flex-col sm:flex-row items-center justify-center gap-6 text-sm text-[hsl(var(--muted-foreground))]">
            <span className="flex items-center gap-1.5"><CheckCircle className="h-4 w-4 text-green-500" /> Sin tarjeta de crédito</span>
            <span className="flex items-center gap-1.5"><CheckCircle className="h-4 w-4 text-green-500" /> 100% conforme con Google</span>
            <span className="flex items-center gap-1.5"><CheckCircle className="h-4 w-4 text-green-500" /> Configuración en 5 minutos</span>
          </div>
        </div>
      </section>

      {/* Social proof bar */}
      <section className="border-y border-[hsl(var(--border))] bg-[hsl(var(--muted))]">
        <div className="mx-auto max-w-6xl px-4 sm:px-6 py-6">
          <div className="flex flex-col sm:flex-row items-center justify-center gap-8 sm:gap-16 text-center">
            <div>
              <p className="text-3xl font-bold text-[hsl(var(--foreground))]">+300%</p>
              <p className="text-sm text-[hsl(var(--muted-foreground))]">Aumento promedio en reseñas</p>
            </div>
            <div className="hidden sm:block h-10 w-px bg-[hsl(var(--border))]" />
            <div>
              <p className="text-3xl font-bold text-[hsl(var(--foreground))]">4.8★</p>
              <p className="text-sm text-[hsl(var(--muted-foreground))]">Calificación promedio de nuestros clientes</p>
            </div>
            <div className="hidden sm:block h-10 w-px bg-[hsl(var(--border))]" />
            <div>
              <p className="text-3xl font-bold text-[hsl(var(--foreground))]">Cd. Juárez</p>
              <p className="text-sm text-[hsl(var(--muted-foreground))]">Y toda la región de Chihuahua</p>
            </div>
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="mx-auto max-w-6xl px-4 sm:px-6 py-20">
        <div className="text-center mb-14">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">Todo lo que necesitas para crecer</h2>
          <p className="text-[hsl(var(--muted-foreground))] max-w-xl mx-auto">
            Una plataforma diseñada específicamente para negocios mexicanos que quieren mejorar su reputación online de forma honesta.
          </p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((f) => (
            <div key={f.title} className="rounded-xl border border-[hsl(var(--border))] p-6 bg-[hsl(var(--card))] hover:shadow-md transition-shadow">
              <div className="h-10 w-10 rounded-lg bg-[hsl(var(--primary))/10] flex items-center justify-center mb-4">
                <f.icon className="h-5 w-5 text-[hsl(var(--primary))]" />
              </div>
              <h3 className="font-semibold text-[hsl(var(--foreground))] mb-2">{f.title}</h3>
              <p className="text-sm text-[hsl(var(--muted-foreground))] leading-relaxed">{f.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* How it works */}
      <section className="bg-[hsl(var(--muted))] py-20">
        <div className="mx-auto max-w-6xl px-4 sm:px-6">
          <div className="text-center mb-14">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">Tan fácil como 1, 2, 3</h2>
            <p className="text-[hsl(var(--muted-foreground))]">Empieza a recibir más reseñas en menos de 10 minutos.</p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {steps.map((s) => (
              <div key={s.n} className="text-center">
                <div className="h-14 w-14 rounded-full bg-[hsl(var(--primary))] text-[hsl(var(--primary-foreground))] flex items-center justify-center mx-auto mb-4 text-xl font-bold">
                  {s.n}
                </div>
                <h3 className="font-semibold text-lg mb-2">{s.title}</h3>
                <p className="text-sm text-[hsl(var(--muted-foreground))]">{s.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Testimonials */}
      <section className="mx-auto max-w-6xl px-4 sm:px-6 py-20">
        <div className="text-center mb-14">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">Negocios que ya están creciendo</h2>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {testimonials.map((t) => (
            <div key={t.name} className="rounded-xl border border-[hsl(var(--border))] p-6 bg-[hsl(var(--card))]">
              <StarRating n={t.stars} />
              <p className="text-sm text-[hsl(var(--foreground))] my-4 leading-relaxed italic">"{t.quote}"</p>
              <div>
                <p className="font-semibold text-sm">{t.name}</p>
                <p className="text-xs text-[hsl(var(--muted-foreground))]">{t.biz}</p>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Compliance badge */}
      <section className="bg-[hsl(var(--primary))/5] border-y border-[hsl(var(--primary))/20] py-12">
        <div className="mx-auto max-w-3xl px-4 sm:px-6 text-center">
          <ShieldCheck className="h-10 w-10 text-[hsl(var(--primary))] mx-auto mb-4" />
          <h3 className="text-xl font-bold mb-2">Trabajamos dentro de las políticas de Google</h3>
          <p className="text-sm text-[hsl(var(--muted-foreground))] max-w-xl mx-auto">
            Nunca compramos, fabricamos ni intercambiamos reseñas. Usamos la API oficial de Google Ads únicamente para análisis de keywords y datos de mercado — sin acceso a cuentas de terceros, sin modificación de campañas. Tu negocio queda 100% protegido.
          </p>
        </div>
      </section>

      {/* CTA */}
      <section className="mx-auto max-w-6xl px-4 sm:px-6 py-24 text-center">
        <h2 className="text-3xl md:text-4xl font-bold mb-4">¿Listo para más reseñas?</h2>
        <p className="text-[hsl(var(--muted-foreground))] mb-8 max-w-md mx-auto">
          Únete a los negocios de Ciudad Juárez y Chihuahua que ya están mejorando su reputación online.
        </p>
        <Button size="lg" className="gap-2">
          Comenzar gratis hoy <ChevronRight className="h-4 w-4" />
        </Button>
      </section>
    </>
  );
}
