#!/usr/bin/env python3
"""Verifica o linie de sah (SAN, engleza) mutare cu mutare.
Uz: python try_line.py "e4 e5 Nf3 Nc6 Bb5 ..."
Optional: al doilea argument = patratul unei piese (ex. b3) => afiseaza mutarile ei legale in pozitia finala.
"""
import sys, chess

def main():
    if len(sys.argv) < 2:
        print("Da o linie de mutari in SAN, ex: \"e4 e5 Nf3 Nc6 Bb5\"")
        return
    moves = sys.argv[1].split()
    watch = sys.argv[2] if len(sys.argv) > 2 else None
    board = chess.Board()
    for i, san in enumerate(moves):
        try:
            mv = board.parse_san(san)
        except Exception as e:
            print(f"  ILEGALA la mutarea #{i+1} '{san}': {e}")
            print(f"  FEN inainte: {board.fen()}")
            return
        board.push(mv)
        tag = ""
        if board.is_checkmate():
            tag = "  <<< MAT"
        elif board.is_check():
            tag = "  (sah)"
        elif board.is_stalemate():
            tag = "  <<< PAT"
        print(f"  {i+1:2d}. {san}{tag}")
    print(f"\nFEN final: {board.fen()}")
    print(f"Mat: {board.is_checkmate()} | Sah: {board.is_check()} | Pat: {board.is_stalemate()}")
    if watch:
        sq = chess.parse_square(watch)
        piece = board.piece_at(sq)
        if piece is None:
            print(f"Nicio piesa pe {watch}.")
        else:
            legal = [board.san(m) for m in board.legal_moves if m.from_square == sq]
            print(f"Piesa pe {watch} = {piece.symbol()}; mutari legale: {legal if legal else 'NICIUNA (blocata/prinsa)'}")

if __name__ == "__main__":
    main()
