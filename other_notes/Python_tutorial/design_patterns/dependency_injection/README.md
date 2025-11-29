# Dependency Injection (DI)

## What is Dependency Injection?

Dependency Injection is a design pattern where an object's dependencies (the components it needs to do its work) are provided from the outside rather than created internally.

This decouples construction from use, making code easier to test, reuse, and maintain.

## Benefits of Dependency Injection

- **Testability:** Injected dependencies can be replaced with mocks or fakes during testing.
- **Loose Coupling:** Components depend on abstractions or externally-provided implementations, reducing tight coupling.
- **Flexibility:** Swapping implementations (e.g., different storage backends) requires minimal code changes.
- **Single Responsibility:** Objects focus on behavior, not on creating dependencies.

## When to Use Dependency Injection

- Use DI when components have external dependencies that vary (databases, network clients, config-driven services).
- Use DI to simplify unit testing and to enable easier substitution of behavior at runtime.
- Use DI in larger systems or libraries where decoupling and extensibility are important.

## Pitfalls of Dependency Injection

- **Overhead:** For very small/simple code, DI can add unnecessary indirection and complexity.
- **Learning Curve:** Teams unfamiliar with DI may misuse it or create overly complex injection setups.
- **Configuration Complexity:** Managing wiring (manual or via a container) can become verbose.

**Quick Python example (constructor injection):**

```py
class EmailSender:
  def send(self, to, subject, body):
    raise NotImplementedError

class SMTPSender(EmailSender):
  def send(self, to, subject, body):
    print(f"Sending email to {to}")

class NotificationService:
  def __init__(self, sender: EmailSender):
    self._sender = sender

  def notify(self, user, message):
    self._sender.send(user.email, "Notice", message)
# Usage: inject the concrete implementation from outside
service = NotificationService(sender=SMTPSender())
service.notify(user, "Hello!")
```

## Summary

Dependency Injection improves modularity, testability, and flexibility by separating how dependencies are created from how they are used.

Use it when you need decoupling and easier testing; avoid it for trivial scripts or where the added indirection isn't justified.
