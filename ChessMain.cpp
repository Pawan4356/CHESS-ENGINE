#include <SDL.h>
#include <iostream>

int main(int argc, char* argv[]) {
    // 1. Initialize SDL
    if (SDL_Init(SDL_INIT_VIDEO) < 0) {
        std::cout << "SDL could not initialize! SDL_Error: " << SDL_GetError() << "\n";
        return 1;
    }

    // 2. Create a window
    SDL_Window* window = SDL_CreateWindow(
        "SDL2 Window",                  // Title
        SDL_WINDOWPOS_CENTERED,         // X position
        SDL_WINDOWPOS_CENTERED,         // Y position
        800,                            // Width
        600,                            // Height
        SDL_WINDOW_SHOWN                // Flags
    );

    if (!window) {
        std::cout << "Window could not be created! SDL_Error: " << SDL_GetError() << "\n";
        SDL_Quit();
        return 1;
    }

    // 3. Create a renderer
    SDL_Renderer* renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);

    // Main loop flag
    bool running = true;

    // Event handler
    SDL_Event e;

    // 4. Game loop
    while (running) {
        // Handle events
        while (SDL_PollEvent(&e) != 0) {
            if (e.type == SDL_QUIT) {
                running = false; // exit loop
            }
        }

        // 5. Clear screen (set color to black)
        SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255);
        SDL_RenderClear(renderer);

        // 6. Draw something (a white rectangle)
        SDL_Rect rect = {200, 150, 400, 300}; // x, y, width, height
        SDL_SetRenderDrawColor(renderer, 255, 255, 255, 255);
        SDL_RenderFillRect(renderer, &rect);

        // 7. Show what we rendered
        SDL_RenderPresent(renderer);
    }

    // 8. Cleanup
    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(window);
    SDL_Quit();

    return 0;
}
