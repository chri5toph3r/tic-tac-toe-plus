# tic-tac-toe-plus

Working version in stable-version branch.

The board is divided into 9 sectors, each sector is divided into 9 tiles which gives 81 tiles in total.
You cannot start in the middle sector.

The game is based on traditional Tic Tac Toe, but it is, you could say, to the power of two.
After one player places his symbole in the specific tile in the sector, 
the second player can place his symbole only in the tile in the sector coresponding to the previously mentioned tile.
E. g.
If your opponent placed his symbole on the sector tile that is in the 1st column and 1st row
you'll be able to place your symbole on the tile which is in 1st column, 1st row sector.

Every time somebody wins a sector, a big symbole of the winner is written on top of it.

Sectors create the 10th "sector" (board), and both players aim to win the board.

Game ends when one of the players wins the board or there is a draw.
