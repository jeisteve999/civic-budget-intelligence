
import asyncio
import io
from contextlib import redirect_stdout, redirect_stderr

from dotenv import load_dotenv
from google.adk.runners import InMemoryRunner
from google.genai import types

from app.agents.root_agent import root_agent


load_dotenv()


async def main():

    print("=" * 70)
    print("CIVIC BUDGET INTELLIGENCE")
    print("=" * 70)

    print(
        "Sistema de investigación y verificación "
        "de información presupuestaria."
    )

    print("Fuente principal: OpenGov Africa - OGA Budget Lens")
    print()
    print("Escribe una pregunta para comenzar.")
    print("Escribe 'salir' para terminar.")
    print("=" * 70)

    runner = InMemoryRunner(
        agent=root_agent,
    )

    # Crear la sesión antes de procesar preguntas
    user_id = "civic_user"
    session_id = "civic_session"

    await runner.session_service.create_session(
        app_name=runner.app_name,
        user_id=user_id,
        session_id=session_id,
    )

    while True:

        question = input("\nPregunta > ").strip()

        if question.lower() in {"salir", "exit", "quit"}:
            print("\nCerrando Civic Budget Intelligence...")
            break

        if not question:
            print("Por favor, escribe una pregunta.")
            continue

        print("\nProcesando...\n")

        final_answer = None

        user_message = types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=question)
            ],
        )

        stdout_buffer = io.StringIO()
        stderr_buffer = io.StringIO()

        try:

            with redirect_stdout(stdout_buffer), redirect_stderr(stderr_buffer):

                async for event in runner.run_async(
                    user_id=user_id,
                    session_id=session_id,
                    new_message=user_message,
                ):
                    if event.author == "analysis_agent":
                        if event.content and event.content.parts:

                            for part in event.content.parts:

                                text = getattr(
                                    part,
                                    "text",
                                    None,
                                )

                                if text:
                                    final_answer = text

            print("-" * 70)
            print("RESPUESTA")
            print("-" * 70)

            if final_answer:
                print(final_answer)
            else:
                print("No se pudo generar una respuesta final.")

            print("-" * 70)

        except Exception as exc:

            print("-" * 70)
            print("ERROR")
            print("-" * 70)
            print(f"No se pudo procesar la pregunta: {exc}")
            print("-" * 70)


if __name__ == "__main__":
    asyncio.run(main())


