A   B       A AND B
-------------------
0   0           0
0   1           0
1   0           0
1   1           1

A   B       A XOR B
-------------------
0   0           0
0   1           1
1   0           1
1   1           0

   1101011
&  1010010
----------
   1000010

    boolean     bitwise
OR   or            |
AND  and           &
XOR  N/A           ^
NOT  not           ~
LEFT SHIFT         <<
RIGHT SHIFT        >>

----------------------

And Masking
  101010101
& 111100000   <-- AND mask
-----------
  101000000


  10100000 ADD
& 11000000
----------
  10000000
  We performed and masking to the ADD instruction
  Now we need to shift the numbers down

  ir = 0b10100000   ADD
  num_oprands == (ir & 0b11000000) >> 6
  dist_to_move_pc = num_operands + 1




