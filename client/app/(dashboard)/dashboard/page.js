export default async function DashboardPage() {
  return (
    <div className="flex min-h-screen bg-zinc-50 font-sans text-zinc-95 dark:text-zinc-50">
      <main className="flex flex-1 flex-col">
        <section className="flex-1 overflow-y-auto bg-linear-to-b from-zinc-50/80 to-zinc-100/80 px-6 py-4 ">
          <div className="mx-auto flex h-full max-w-3xl flex-col gap-3"></div>
        </section>
      </main>
    </div>
  );
}
