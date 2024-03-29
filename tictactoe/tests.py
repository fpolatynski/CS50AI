from tictactoe import initial_state, player, actions, result, winner, terminal, utility

X = "X"
O = "O"
EMPTY = None

a = [[EMPTY, EMPTY, EMPTY],
    [EMPTY, X, EMPTY],
    [EMPTY, EMPTY, EMPTY]]
a1  = [[O, EMPTY, EMPTY],
    [EMPTY, X, EMPTY],
    [EMPTY, EMPTY, EMPTY]]

a2  = [[O, EMPTY, X],
    [EMPTY, X, X],
    [EMPTY, EMPTY, X]]

b = [[EMPTY, X, EMPTY],
    [EMPTY, X, O],
    [EMPTY, X, O]]


b1 = [[O, O, O],
    [X, X, EMPTY],
    [X, X, O]]

b2 = [[X, O, O],
    [EMPTY, X, O],
    [EMPTY, X, X]]
b3 = [[X, O, X],
    [X, O, O],
    [O, X, X]]


def test_player():
    assert player(a) == O
    assert player(initial_state()) == X
    assert player(b) == O


def test_actions():
    assert len(actions(initial_state())) == 9
    assert len(actions(a)) == 8
    assert len(actions(b)) == 4


def test_result():
    assert result(a, (0, 0)) == a1


def test_winner():
    assert winner(b) == X
    assert winner(b1) == O
    assert winner(b2) == X


def test_terminal():
    assert terminal(b2) == True
    assert terminal(b3) == True
    assert terminal(a) == False


def test_utility():
    assert utility(b3) == 0
    assert utility(b2) == 1
    assert utility(b1) == -1

