import copy
from operator import add
import random
import pygame

pygame.init()

card_values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

#symbolen toevoegen aan kaarten
card_suits = ['♠', '♥', '♦', '♣']
one_deck = 4 * card_values

one_deck = []
for suit in card_suits:
    for value in card_values:
        one_deck.append((value, suit))
decks = 4
WIDTH = 600
HEIGHT = 900
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Pygame Blackjack!')
fps = 60
timer = pygame.time.Clock()
# font aanpassen om symbolen zichtbaar te maken
font = pygame.font.SysFont("segoe ui symbol", 32)

# Tutorial font toevoegen aangepast aan het scherm
tutorial_font = pygame.font.SysFont("segoe ui symbol", 24)
tutorial_font.set_bold(True)
smaller_font = pygame.font.SysFont("segoe ui symbol", 20)
result_font = pygame.font.SysFont("segoe ui symbol", 30)
result_font .set_italic(True)
active = False
show_tutorial = True
dealer_name = "Casino Bot"

records = [0, 0, 0]
player_score = 0
dealer_score = 0

# toevoegen "chaos mode"
target_score = 21

# kaarten animatie toevoegen
card_animation = 0
dealer_animation = 0
initial_deal = False
my_hand = []
dealer_hand = []
outcome = 0
reveal_dealer = False
hand_active = False
outcome = 0
add_score = False
results = ['', 'PLAYER BUSTED o_O', 'Player WINS! :)', 'DEALER WINS :(', 'TIE GAME...']


def deal_cards(current_hand, current_deck):
    card = random.randint(0, len(current_deck))
    current_hand.append(current_deck[card - 1])
    current_deck.pop(card - 1)
    return current_hand, current_deck



def draw_scores(player, dealer):
    screen.blit(
        smaller_font.render(dealer_name, True, "gold"),
        (20,10)
    )
    screen.blit(
        font.render(f'Score[{player}]', True, 'white'),
        (350, 400)
    )
    if reveal_dealer:
        screen.blit(
            font.render(f'Score[{dealer}]', True, 'white'),
            (400, 140)
        ) 


def draw_cards(player, dealer, reveal):
    for i in range(len(player)):
        y_pos = 460 +(5*i)

        if i == len(player) - 1:
            y_pos+=card_animation
        pygame.draw.rect(
            screen,
            'white',
            [70 + (70 * i), y_pos, 120, 220],
            0,
            5
        )
        # functie verwacht een string maar moet een tuple zijn
        card_text=f"{player[i][0]}{player[i][1]}"
        suit = player [i][1]
        card_color = "red" if suit in ['♥', '♦'] else "black"
        screen.blit(
            font.render(card_text, True, card_color),
            (75 + 70 * i, y_pos +5)
        )
        screen.blit(
            font.render(card_text, True, card_color),
            (75 + 70 * i, y_pos + 175)
        )
        pygame.draw.rect(
            screen, 
            'black',
            [70 + (70 * i), y_pos, 120, 220],
            5,
            5
           )

    
    for i in range(len(dealer)):
        dealer_y = 160 +(5*i)

        if i == len(dealer) - 1:
            dealer_y+=dealer_animation
        pygame.draw.rect(
            screen,
            'white',
            [70 + (70 * i), dealer_y, 120, 220],
            0,
            5
        )
        if i != 0 or reveal:
            card_text = f"{dealer[i][0]}{dealer[i][1]}"
            suit = dealer [i][1]
            card_color = "red" if suit in ['♥', '♦'] else "black"
            screen.blit(
                font.render(card_text, True, card_color),
                (75 + 70 * i, dealer_y + 5)
            )
            screen.blit(
                font.render(card_text, True, card_color),
                (75 + 70 * i, dealer_y + 175)
            )
        else:
            screen.blit(font.render('???', True, 'black'), (75 + 70 * i, 165 + 5 * i))
            screen.blit(font.render('???', True, 'black'), (75 + 70 * i, 335 + 5 * i))
        pygame.draw.rect(
            screen, 
            'black',
            [70 + (70 * i), dealer_y, 120, 220],
            5,
            5
           )    


def calculate_score(hand):
    hand_score = 0
    aces_count = sum(1 for card in hand if card[0] ==  'A')

    for card in hand: 
        card_value = card[0]

        if card_value in ['2', '3', '4', '5', '6', '7', '8', '9']:
            hand_score += int(card_value)

        elif card_value in ['10','J', 'Q', 'K']:
            hand_score += 10
        
        elif card_value == 'A':
            hand_score += 11

    while hand_score > target_score and aces_count > 0:
        hand_score -= 10
        aces_count -= 1 
    
    return hand_score

def draw_game(act, record, result):
    button_list = []

    #hoverfunctie toevoegen aan knoppen
    mouse_pos = pygame.mouse.get_pos()
    # initially on startup (not active) only option is to deal new hand
    if not act:
        deal_color = "white"

        if pygame.Rect(150, 20, 300, 100).collidepoint(mouse_pos):
            deal_color = "lightgreen"

        deal = pygame.draw.rect(
            screen, 
            deal_color, 
            [150, 20, 300, 100],
            0,
            5
        )
        
        pygame.draw.rect(screen, 'green', [150, 20, 300, 100], 3, 5)
        deal_text = font.render('DEAL HAND', True, 'black')
        screen.blit(deal_text, (165, 50))

        button_list.append(deal)

   
    else:
        hit_color = "white"
        hit_y = 700
        if pygame.Rect(0, 700, 300, 100).collidepoint(mouse_pos):
            hit_color = "lightgray"
            hit_y = 690

        hit = pygame.draw.rect(
            screen,
            hit_color, 
            [0, hit_y, 300, 100],
            0,
            5
        )
        pygame.draw.rect(screen, 'green', [0, hit_y, 300, 100], 3, 5)
        hit_text = font.render('HIT ME', True, 'black')
        screen.blit(hit_text, (55, hit_y + 35))
        button_list.append(hit)

        stand_color = "white"
        stand_y = 700
        if pygame.Rect(300, 700, 300, 100).collidepoint(mouse_pos):
            stand_color = "lightgray"
            stand_y = 690
        stand = pygame.draw.rect(
            screen,
            stand_color,
            [300, stand_y, 300, 100],
            0,
            5
        )
        pygame.draw.rect(screen, 'green', [300, stand_y, 300, 100], 3, 5)
        stand_text = font.render('STAND', True, 'black')
        screen.blit(stand_text, (355, stand_y + 35))
        button_list.append(stand)
        score_text = smaller_font.render(f'Wins: {record[0]}   Losses: {record[1]}   Draws: {record[2]}', True, 'white')
        screen.blit(score_text, (15, 840))
    
    if result != 0:
        screen.blit(result_font.render(results[result], True, 'white'), (15, 25))
        deal = pygame.draw.rect(screen, 'white', [300, 20, 300, 100], 0, 5)
        pygame.draw.rect(screen, 'green', [300, 20, 300, 100], 3, 5)
        pygame.draw.rect(screen, 'black', [303, 20, 294, 94], 3, 5)
        deal_text = font.render('NEW HAND', True, 'black')
        text_rect = deal_text.get_rect(center=deal.center)
        screen.blit(deal_text, text_rect)
        button_list.append(deal)
    return button_list

def check_endgame(hand_act, deal_score, play_score, result, totals, add):
    if not hand_act and deal_score >= 17:
        if play_score > target_score:
            result = 1
        elif deal_score < play_score <= target_score:
            result = 2
        elif play_score < deal_score <= target_score:
            result = 3
        else:
            result = 4
        if add:
            if result == 1 or result == 3:
                totals[1] += 1
            elif result == 2:
                totals[0] += 1
            else:
                totals[2] += 1
            add = False
            
    return result, totals, add 

# Tutorial toevoegen met uitleg Hit en Stand

def draw_tutorial():
    screen.fill((20, 80, 20))

    title = font.render("BLACKJACK TUTORIAL", True, "white")
    screen.blit(title, (40, 50))

    line1 = tutorial_font.render("Welkom bij Blackjack!", True, "white")
    line2 = tutorial_font.render("Probeer zo dicht mogelijk bij 21 (of 22,23) te komen.", True, "white")
    line3 = tutorial_font.render("Hit = neem een extra kaart.", True, "white")
    line4 = tutorial_font.render("Stand = stop met kaarten nemen.", True, "white")

    screen.blit(line1, (40, 180))
    screen.blit(line2, (40, 240))
    screen.blit(line3, (40, 300))
    screen.blit(line4, (40, 360))

   # Hover aanpassen voor startknop - groter wordt als je pijl erop komt. 
    mouse_pos = pygame.mouse.get_pos()

    button_x = 100
    button_y = 650
    button_width = 400
    button_height = 100

    if pygame.Rect(button_x, button_y, button_width, button_height).collidepoint(mouse_pos):
        button_x = 90
        button_y = 640
        button_width = 420
        button_height = 120

    start_button = pygame.draw.rect(
        screen, 
        "white",
        [button_x, button_y, button_width, button_height],
    )
    pygame.draw.rect(
        screen,
        "Gold",
        [button_x, button_y, button_width, button_height],
        4
    )

    if pygame.Rect(button_x, button_y, button_width, button_height).collidepoint(mouse_pos):
        button_text_font = pygame.font.SysFont("segoe ui symbol", 30)
        button_text_font.set_bold(True)
    else:
        button_text_font = pygame.font.SysFont("segoe ui symbol", 24)
        button_text_font.set_bold(True)

    start_text = button_text_font.render("START GAME", True, "forest green")

    text_rect = start_text.get_rect(center=start_button.center)
    screen.blit(start_text, text_rect)

    return start_button

run = True
while run:

    if show_tutorial:
        tutorial_button = draw_tutorial()
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONUP:
                if tutorial_button.collidepoint(event.pos):
                    show_tutorial = False

        continue

    timer.tick(fps)
    if card_animation > 0:
        card_animation -= 1

    if dealer_animation > 0:
        dealer_animation -= 2
    screen.fill('black')

    # achtergrond aanpassen 
    screen.fill((0,50,0))

    if initial_deal:
        for i in range(2):
            my_hand, game_deck = deal_cards(my_hand, game_deck)
            dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
        initial_deal = False
    
    if active:
        player_score = calculate_score(my_hand)
        print(my_hand)
        draw_cards(my_hand, dealer_hand, reveal_dealer)
        if reveal_dealer:
            dealer_score = calculate_score(dealer_hand)
            if dealer_score < target_score - 4:
                dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
                dealer_animation = 30
        draw_scores(player_score, dealer_score)
    buttons = draw_game(active, records, outcome)

    target_text = smaller_font.render(
        f"Target: {target_score}",
        True,
        "Yellow"
    )
    screen.blit(target_text,(20,130))

    # event handling, if quit pressed, then exit game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONUP:
            if not active:
                if buttons[0].collidepoint(event.pos):
                    active = True
                    initial_deal = True
                    # bij elke nieuwe hand een eindscore kiezen
                    target_score = random.choice([21,22,23])
                    game_deck = copy.deepcopy(decks * one_deck)
                    my_hand = []
                    dealer_hand = []
                    outcome = 0
                    hand_active = True
                    reveal_dealer = False
                    outcome = 0
                    add_score = True
            else:
                # if player can hit, allow them to draw a card
                if buttons[0].collidepoint(event.pos) and player_score < target_score and hand_active:
                    my_hand, game_deck = deal_cards(my_hand, game_deck)
                    #kaart animatie toevoegen
                    card_animation = 40
                # allow player to end turn (stand)
                elif buttons[1].collidepoint(event.pos) and not reveal_dealer:
                    reveal_dealer = True
                    hand_active = False
                elif len(buttons) == 3:
                    if buttons[2].collidepoint(event.pos):
                        target_score = random.choice([21,22,23])
                        active = True
                        initial_deal = True                
                        game_deck = copy.deepcopy(decks * one_deck)
                        my_hand = []
                        dealer_hand = []
                        outcome = 0
                        hand_active = True
                        reveal_dealer = False
                        outcome = 0
                        add_score = True
                        dealer_score = 0
                        player_score = 0

    if hand_active and player_score > target_score:
        hand_active = False
        reveal_dealer = True

    outcome, records, add_score = check_endgame(hand_active, dealer_score, player_score, outcome, records, add_score)

    pygame.display.flip()
pygame.quit()
