import { createFileRoute } from "@tanstack/react-router";
import { Star, Target, ShieldCheck, BarChart3 } from "lucide-react";

export const Route = createFileRoute("/nosotros")({
  component: Nosotros,
});

function Nosotros() {
  return (
    <div className="mx-auto max-w-4xl px-4 sm:px-6 py-16">
      <div className="text-center mb-14">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-[hsl(var(--primary))/10] text-[hsl(var(--primary))] text-sm font-medium mb-4">
          <Star className="h-3.5 w-3.5 fill-current" />
          Somos de aquí
        </div>
        <h1 className="text-4xl md:text-5xl font-bold mb-4">Quiénes somos</h1>
        <p className="text-[hsl(var(--muted-foreground))] text-lg max-w-2xl mx-auto">
          MejoresReseñas nació en Ciudad Juárez para resolver un problema real que vimos en cientos de negocios locales: muchos ofrecen un servicio excelente pero nadie lo sabe porque no tienen reseñas.
        </p>
      </div>

      <div className="prose prose-neutral max-w-none space-y-6 mb-16 text-[hsl(var(--foreground))]">
        <h2 className="text-2xl font-bold">Nuestra misión</h2>
        <p className="text-[hsl(var(--muted-foreground))] leading-relaxed">
          Ayudar a negocios locales en México — restaurantes, talleres, salones de belleza, clínicas, tiendas — a construir una reputación online sólida y auténtica que los ayude a crecer. No vendemos trucos; vendemos resultados honestos.
        </p>

        <h2 className="text-2xl font-bold">Lo que nos diferencia</h2>
        <p className="text-[hsl(var(--muted-foreground))] leading-relaxed">
          Somos la única plataforma enfocada específicamente en el mercado de Ciudad Juárez y Chihuahua. Entendemos las dinámicas del comercio local, el comportamiento del consumidor en la región y los giros de negocio más comunes. Nuestros datos de keyword y análisis de mercado reflejan búsquedas reales en esta zona, no promedios nacionales.
        </p>

        <h2 className="text-2xl font-bold">Cómo usamos la tecnología</h2>
        <p className="text-[hsl(var(--muted-foreground))] leading-relaxed">
          Usamos la API oficial de Google Ads para analizar datos de volumen de búsqueda de keywords locales. Este acceso es de solo lectura y se usa exclusivamente para investigación de mercado — para entender qué buscan tus clientes, no para gestionar campañas publicitarias. Ningún dato de clientes finales es compartido con terceros.
        </p>
        <p className="text-[hsl(var(--muted-foreground))] leading-relaxed">
          Además usamos la API de Google Business Profile con consentimiento explícito de cada negocio, para leer métricas de desempeño de su perfil. Cada negocio decide qué información compartir y puede revocar el acceso en cualquier momento.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-16">
        {[
          { icon: Target, title: "Enfoque local", desc: "Datos y análisis específicos para Ciudad Juárez, Chihuahua y el norte de México." },
          { icon: ShieldCheck, title: "Cumplimiento total", desc: "Operamos 100% dentro de las políticas de uso de Google. Sin riesgos para tu negocio." },
          { icon: BarChart3, title: "Basado en datos", desc: "Cada recomendación que hacemos está respaldada por datos de búsqueda reales, no suposiciones." },
        ].map((v) => (
          <div key={v.title} className="rounded-xl border border-[hsl(var(--border))] p-6 bg-[hsl(var(--card))] text-center">
            <div className="h-12 w-12 rounded-full bg-[hsl(var(--primary))/10] flex items-center justify-center mx-auto mb-4">
              <v.icon className="h-6 w-6 text-[hsl(var(--primary))]" />
            </div>
            <h3 className="font-semibold mb-2">{v.title}</h3>
            <p className="text-sm text-[hsl(var(--muted-foreground))]">{v.desc}</p>
          </div>
        ))}
      </div>

      <div className="rounded-xl bg-[hsl(var(--muted))] p-8 text-center">
        <h3 className="text-xl font-bold mb-2">¿Tienes preguntas o quieres saber más?</h3>
        <p className="text-[hsl(var(--muted-foreground))] mb-4">Escríbenos directamente. Respondemos el mismo día.</p>
        <a
          href="mailto:contacto@mejoresreviews.com"
          className="text-[hsl(var(--primary))] font-medium hover:underline"
        >
          contacto@mejoresreviews.com
        </a>
      </div>
    </div>
  );
}
