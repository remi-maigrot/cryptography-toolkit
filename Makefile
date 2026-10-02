##
## EPITECH PROJECT, 2023
## B-CNA-500-BDX-5-1-cryptography-remi.maigrot
## File description:
## Makefile
##

SRC		=	./src/

NAME	=	mypgp

all		:	$(NAME)

$(NAME) :
			cp $(SRC)main.py ./
			mv main.py $(NAME)
			chmod +x $(NAME)

clean	:
			rm -rf $(NAME)

fclean	:	clean

re		:	fclean all

.PHONY: all clean fclean re
