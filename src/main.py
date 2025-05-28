# -*- coding: utf-8 -*-
import sys, time, random
import freenect
import numpy as np
import cv2
import pygame
from particle import Particle

# Configuration
WIDTH, HEIGHT = 640, 480
THRESHOLD = 30      # seuil de détection de mouvement
SPAWN_RATE = 100    # nombre de particules à générer par frame
MAX_PARTICLES = 500

def get_depth():
    depth, _ = freenect.sync_get_depth()
    # normaliser en 8-bit pour faciliter le traitement
    depth8 = np.uint8(depth.astype(np.float32) * 255.0 / 2048.0)
    return depth8

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pattern Kinect-Pi")
    clock = pygame.time.Clock()

    prev_depth = None
    particles = []

    try:
        while True:
            # 1) Capture
            depth = get_depth()

            # 2) Mouvement
            if prev_depth is None:
                diff = np.zeros_like(depth)
            else:
                diff = cv2.absdiff(depth, prev_depth)
            prev_depth = depth.copy()

            # 3) Masque de mouvement
            _, mask = cv2.threshold(diff, THRESHOLD, 255, cv2.THRESH_BINARY)
            ys, xs = np.where(mask > 0)

            # 4) Génération de particules
            for _ in range(min(SPAWN_RATE, len(xs))):
                idx = random.randrange(len(xs))
                x = xs[idx] * WIDTH // mask.shape[1]
                y = ys[idx] * HEIGHT // mask.shape[0]
                angle = random.uniform(0, 2*np.pi)
                speed = random.uniform(1,3)
                vx, vy = speed * np.cos(angle), speed * np.sin(angle)
                color = (random.randint(100,255), random.randint(100,255), random.randint(100,255))
                particles.append(Particle((x,y), (vx,vy), color))

            # 5) Mise à jour
            for p in particles:
                p.update()
            particles = [p for p in particles if p.is_alive()]
            if len(particles) > MAX_PARTICLES:
                particles = particles[-MAX_PARTICLES:]

            # 6) Affichage
            # légère traînée
            screen.fill((0,0,0,20))
            for p in particles:
                p.draw(screen)
            pygame.display.flip()

            # 7) Gestion événements
            for e in pygame.event.get():
                if e.type == pygame.QUIT or (e.type==pygame.KEYDOWN and e.key==pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()

            clock.tick(15)  # ~15 FPS

    except Exception as e:
        print("Erreur :", e)
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()
