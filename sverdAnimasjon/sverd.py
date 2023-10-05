#%%
import pygame
import sys
import os

# Initialiser Pygame
pygame.init()

# Skjermstørrelse
skjerm_bredde = 800
skjerm_høyde = 600

# Farger
hvit = (255, 255, 255)
svart = (0, 0, 0)
rød = (255, 0, 0)

# Opprett et vindu
skjerm = pygame.display.set_mode((skjerm_bredde, skjerm_høyde))
pygame.display.set_caption("Bevegelsesanimasjon")

# Spillerens posisjon og egenskaper
FPS = 60
spiller_bredde = 20
spiller_høyde = 40
spiller_x = 50
spiller_y = 450
spiller_hastighet = 5
hopp_høyde = 10
hopp = False
går_venstre = False
går_høyre = False

# Angrepsvariabler
angrep_bilder = []  # Liste for å lagre angrepsanimasjonsbildene
angrep_indeks = 0
angrep_delay = 80  # Tidsforsinkelse mellom hvert bilde (i millisekunder)
angrep_animasjon = False


# Standardbilde før og etter angrep
standard_bilde = pygame.image.load(os.path.join('game', 'angrep_animasjon', "still.png"))


# Last inn angrepsanimasjonsbildene
for i in range(1, 7):  # Antall bilder (1 til 6)
    bilde_navn = os.path.join('game', 'angrep_animasjon',f"attack{i}.png")
    bilde = pygame.image.load(bilde_navn)
    angrep_bilder.append(bilde)

# Hovedspill løkke
clock = pygame.time.Clock()
while True:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Håndter tastetrykk for å starte angrepet
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                hopp = True
            if event.key == pygame.K_a and not angrep_animasjon:
                angrep_animasjon = True

            if event.key == pygame.K_LEFT:
                går_venstre = True
            if event.key == pygame.K_RIGHT:
                går_høyre = True

        # Håndter tastetrykk for å stoppe bevegelsen
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                går_venstre = False
            if event.key == pygame.K_RIGHT:
                går_høyre = False

    # Bevegelse av spilleren
    if går_venstre and spiller_x > 0:
        spiller_x -= spiller_hastighet
    if går_høyre and spiller_x < skjerm_bredde - spiller_bredde:
        spiller_x += spiller_hastighet

    # Hoppemekanikk
    if hopp:
        if hopp_høyde >= -10:
            neg = 1
            if hopp_høyde < 0:
                neg = -1
            spiller_y -= (hopp_høyde ** 2) * 0.5 * neg
            hopp_høyde -= 1
        else:
            hopp = False
            hopp_høyde = 10

    # Angrepsmekanikk
    if angrep_animasjon:
        if angrep_indeks < len(angrep_bilder):
            skjerm.fill(hvit)
            if går_høyre:  # Sjekk om spilleren går til høyre
                skjerm.blit(angrep_bilder[angrep_indeks], (spiller_x - 30, spiller_y - 55))  # Angrep til venstre
            elif  går_venstre:  # Sjekk om spilleren går til venstre
                skjerm.blit(pygame.transform.flip(angrep_bilder[angrep_indeks], True, False), (spiller_x, spiller_y - 55))  # Angrep til høyre (speilvendt bilde)
                
            pygame.display.update()
            pygame.time.delay(angrep_delay)  # Forsinkelse mellom hvert bilde
            angrep_indeks += 1
        else:
            angrep_animasjon = False
            angrep_indeks = 0
    else:
        # Vis standardbilde når ikke i angrep
        skjerm.fill(hvit)
        if går_venstre:
            skjerm.blit(pygame.image.load(os.path.join('game', 'angrep_animasjon',"go_left.png")), (spiller_x, spiller_y))
        elif går_høyre:
            skjerm.blit(pygame.image.load(os.path.join('game', 'angrep_animasjon',"go_right.png")), (spiller_x, spiller_y))
        else:
            skjerm.blit(standard_bilde, (spiller_x, spiller_y))  # Posisjon for standardbilde

    # Oppdater skjermen
    pygame.display.update()
# %%
