# Hardware and IoT Projects

## Build strategy

Prove the riskiest physical interaction first: sensor reading, actuator control, power behavior, connectivity, or timing. Keep a simulator or recorded telemetry path available for the demo.

## Safety

- Stay within component voltage, current, temperature, and mechanical limits.
- Do not prototype unsafe mains-voltage, medical, vehicle-control, or high-energy systems without qualified supervision.
- Add explicit safe states for disconnects, invalid sensor values, and software crashes.
- Keep credentials and device secrets out of firmware repositories.

## Demo readiness

Bring spare cables, adapters, batteries, components, and an offline build. Label the physical system clearly and make the software state visible on screen so judges can follow the interaction.
