import os
import geometric_lib.circle as circle
import geometric_lib.square as square

def main() :
  r = int(os.getenv("RADIUS", "1"))
  s = int(os.getenv("SIDE", "1"))

  print(f"Circle area (r = {r}) : {circle.area(r)}")
  print(f"Square perimeter (p = {s}) : {square.area(s)}")

if __name__ == "__main__":
  main()