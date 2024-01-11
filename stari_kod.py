def generate_individual(self):
        first_row = ['' for _ in range(8)] # kreiramo prazan

        rook_positions = random.sample(range(8), 2) # prvo biramo dve pozicije za topove
        while abs(rook_positions[0] - rook_positions[1]) == 1: # ne smeju biti jedan pored drugog, jer izmedju mora kralj
            rook_positions = random.sample(range(8), 2)
        first_row[rook_positions[0]] = ROOK
        first_row[rook_positions[1]] = ROOK

        # Odaberi bilo koje mesto između ta dva topa za kralja
        if rook_positions[0] < rook_positions[1]:
            king_position = random.choice(range(rook_positions[0] + 1, rook_positions[1]))
        else:
            king_position = random.choice(range(rook_positions[1] + 1, rook_positions[0]))
        first_row[king_position] = KING

        # Postavljamo lovce na polja različitih boja
        valid_positions = set(range(8)) - set([king_position] + rook_positions)
        bishop_positions = random.sample(list(valid_positions), 2)
        while abs(bishop_positions[0] - bishop_positions[1]) % 2 == 0: # ne smeju biti na pozicijama iste boje
            bishop_positions = random.sample(list(valid_positions), 2)
        first_row[bishop_positions[0]] = BISHOP
        first_row[bishop_positions[1]] = BISHOP

        # Postavljamo kraljicu i konje
        valid_positions -= set(bishop_positions)
        queen_position = random.choice(list(valid_positions))
        first_row[queen_position] = QUEEN
        valid_positions -= set([queen_position])
        valid_positions = list(valid_positions)
        first_row[valid_positions[0]] = KNIGHT
        first_row[valid_positions[1]] = KNIGHT

        return first_row