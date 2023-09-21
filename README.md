# CRAFT: Lightweight Tweakable Block Cipher with Efficient Protection Against DFA Attacks

[Original paper](https://orbilu.uni.lu/handle/10993/39112)

Tweakability is achieved by XORing the key with the tweak and a permutation of the key during key initialization. This is generally undesirable, for performance and security reasons.

For performance, it is desirable to be able to change the tweak without needing to reiniitalize the keys. Key initialization or key expansion is the step where the given key is converted to subkeys actually used during the round functions, and this is often a expensive step in terms of performance. Typically this is done once for each key, after which many encryption/decryption operations can be performed. By using the tweak in the key initialization step, this has to be repeated for every key/tweak combination. However, the key expansion of CRAFT is quite simple and fast, so in CRAFT this performance hit is limited. In the paper, the key initialization is described in 4.5, "Key and Tweak Schedule".

For security, it is risky to relate the key to the tweak, because of related-key attacks. In an attack model where the tweak is under control of the attacker, an attacker can encrypt with two related tweaks, which will result in related subkeys. This can be helpful in exploiting a related-key attack and recover the key.

Several sources already warn about simply XORing the tweak with the key. CRAFT uses a simple permutation of the tweak on top of this, but it is not clear why this would be sufficient.

[Liskov, Moses, Ronald L. Rivest, and David Wagner. "Tweakable block ciphers."](https://escholarship.org/content/qt311931t6/qt311931t6.pdf):

> xoring the tweak into the key ... need not yield secure tweakable block ciphers, since a block cipher need not
depend on every bit of its key. (Biham’s related-key attacks of Biham [3] would
be relevant to this sort of design.)

[Jean, Jérémy, Ivica Nikolić, and Thomas Peyrin. "Tweaks and keys for block ciphers: the TWEAKEY framework."](https://eprint.iacr.org/2014/831.pdf):

> Simple constructions of a tweakable block cipher EK(T, P) based on a block cipher EK(P), like
XORing the tweak into the key input and/or message input, are not satisfactory.

The simple key and tweak expansion opens the door to related-key attacks, and indeed CRAFT has been found to be vulnerable:

[ElSheikh, Muhammad, and Amr M. Youssef. "Related-key differential cryptanalysis of full round CRAFT."](https://eprint.iacr.org/2019/932.pdf)
