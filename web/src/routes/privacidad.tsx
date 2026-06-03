import { createFileRoute } from "@tanstack/react-router";

export const Route = createFileRoute("/privacidad")({
  component: Privacidad,
});

function Section({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <section className="mb-10">
      <h2 className="text-xl font-bold mb-3 text-[hsl(var(--foreground))]">{title}</h2>
      <div className="text-[hsl(var(--muted-foreground))] space-y-3 leading-relaxed text-sm">{children}</div>
    </section>
  );
}

function Privacidad() {
  return (
    <div className="mx-auto max-w-3xl px-4 sm:px-6 py-16">
      <h1 className="text-4xl font-bold mb-2">Política de Privacidad</h1>
      <p className="text-sm text-[hsl(var(--muted-foreground))] mb-12">
        Última actualización: 2 de junio de 2026 · MejoresReseñas · Ciudad Juárez, Chihuahua, México
      </p>

      <Section title="1. Quiénes somos">
        <p>
          MejoresReseñas ("nosotros", "nuestra plataforma") es un servicio operado desde Ciudad Juárez, Chihuahua, México. Nos dedicamos a ayudar a negocios locales a conseguir más reseñas auténticas en Google y a mejorar su visibilidad en Google Maps, siempre dentro de las políticas de Google.
        </p>
        <p>Contacto: <a href="mailto:contacto@mejoresreviews.com" className="text-[hsl(var(--primary))] hover:underline">contacto@mejoresreviews.com</a></p>
      </Section>

      <Section title="2. Información que recopilamos">
        <p><strong className="text-[hsl(var(--foreground))]">Información de negocios:</strong> Nombre del negocio, dirección, categoría, número de reseñas y calificación promedio de tu Perfil de Google Business — solo si otorgas acceso explícito mediante OAuth.</p>
        <p><strong className="text-[hsl(var(--foreground))]">Datos de uso de la plataforma:</strong> Páginas visitadas, acciones realizadas dentro de la plataforma (por ejemplo, cuántas solicitudes de reseña se enviaron) y datos de sesión.</p>
        <p><strong className="text-[hsl(var(--foreground))]">Datos de mercado (no personales):</strong> Usamos la API de Google Ads para obtener volúmenes de búsqueda de keywords relacionadas con reseñas y reputación local. Estos datos son agregados y no contienen información de usuarios finales.</p>
        <p><strong className="text-[hsl(var(--foreground))]">Lo que NO recopilamos:</strong> No almacenamos información personal de los clientes de tu negocio. No tenemos acceso a tus campañas de Google Ads. No leemos tus conversaciones privadas.</p>
      </Section>

      <Section title="3. Uso de la API de Google Ads">
        <p>
          Usamos la API de Google Ads exclusivamente para consultar datos de volumen de búsqueda de keywords mediante el método <code className="bg-[hsl(var(--muted))] px-1 rounded text-xs">generateKeywordHistoricalMetrics</code> del servicio <code className="bg-[hsl(var(--muted))] px-1 rounded text-xs">KeywordPlanIdeaService</code>. Este acceso es:
        </p>
        <ul className="list-disc pl-5 space-y-1">
          <li>De solo lectura — no modificamos ninguna campaña ni configuración de cuentas.</li>
          <li>Usado únicamente para investigación de mercado interna sobre términos de búsqueda locales.</li>
          <li>Limitado a datos de keywords — no accedemos a datos de clientes, conversiones ni rendimiento de anuncios de terceros.</li>
          <li>Operado con un token de desarrollador de Google Ads registrado y aprobado.</li>
        </ul>
      </Section>

      <Section title="4. Uso de la API de Google Business Profile">
        <p>
          Accedemos a tu Perfil de Google Business únicamente cuando tú autorizas explícitamente mediante el flujo de OAuth 2.0 de Google. Los datos que leemos incluyen: métricas de rendimiento del perfil (impresiones, llamadas, solicitudes de ruta), keywords de búsqueda que activan tu perfil y calificación promedio.
        </p>
        <p>
          Puedes revocar este acceso en cualquier momento desde tu cuenta de Google en: myaccount.google.com/permissions.
        </p>
      </Section>

      <Section title="5. Cómo usamos tu información">
        <ul className="list-disc pl-5 space-y-1">
          <li>Para mostrar tu panel de métricas dentro de la plataforma.</li>
          <li>Para generar recomendaciones personalizadas sobre cómo mejorar tu perfil de Google.</li>
          <li>Para análisis internos de uso del servicio (de forma agregada y anónima).</li>
          <li>Para enviarte notificaciones sobre nuevas reseñas (solo si activas esta función).</li>
        </ul>
        <p>No vendemos, arrendamos ni compartimos tu información con terceros para fines de marketing.</p>
      </Section>

      <Section title="6. Retención y eliminación de datos">
        <p>
          Los datos de tu perfil de negocio se conservan mientras tengas una cuenta activa. Al cerrar tu cuenta eliminamos todos tus datos en un plazo de 30 días. Puedes solicitar la eliminación anticipada escribiéndonos a <a href="mailto:contacto@mejoresreviews.com" className="text-[hsl(var(--primary))] hover:underline">contacto@mejoresreviews.com</a>.
        </p>
      </Section>

      <Section title="7. Cookies y tecnologías similares">
        <p>
          Usamos cookies esenciales para el funcionamiento de la sesión y cookies analíticas (Google Analytics) para entender cómo se usa la plataforma. No usamos cookies de publicidad personalizada.
        </p>
      </Section>

      <Section title="8. Seguridad">
        <p>
          Almacenamos credenciales de acceso de forma encriptada. Los tokens de OAuth se guardan en almacenamiento seguro y nunca se registran en logs de texto plano. Realizamos auditorías de seguridad periódicas.
        </p>
      </Section>

      <Section title="9. Tus derechos">
        <p>Tienes derecho a acceder, corregir y eliminar tu información. Para ejercer estos derechos escríbenos a <a href="mailto:contacto@mejoresreviews.com" className="text-[hsl(var(--primary))] hover:underline">contacto@mejoresreviews.com</a>. Respondemos en un máximo de 5 días hábiles.</p>
      </Section>

      <Section title="10. Cambios a esta política">
        <p>
          Notificaremos cambios materiales a esta política por correo electrónico con al menos 15 días de anticipación. El uso continuado de la plataforma después de ese periodo constituye aceptación de los cambios.
        </p>
      </Section>

      <Section title="11. Contacto">
        <p>MejoresReseñas · Ciudad Juárez, Chihuahua, México</p>
        <p>Correo: <a href="mailto:contacto@mejoresreviews.com" className="text-[hsl(var(--primary))] hover:underline">contacto@mejoresreviews.com</a></p>
      </Section>
    </div>
  );
}
