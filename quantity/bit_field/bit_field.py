# -*- coding: utf-8 -*-
"""
Numbers as BitField, this class is useful on its own, it is very useful as a superclass.

>>> class MyField(BitField):
>>>     @property
>>>     def subField(self):
>>>         return self[2:5]
>>>     @subField.setter
>>>     def subField(self, value):
>>>         self[2:5] = value
>>> x = MyField(0x14)
>>> x.subField
5
>>> x.subField = 7
>>> x.subField
7
>>> hex(int(x))
0x1c
"""
__author__ = "akm"


class BitField:
    """
    Represents an arbitrary length bit field as a sliceable value

    .. Note:
    arbitrary means up to 1280 bits in this case

    :param value: Initial value
    """
    __slots__ = ('__value',)

    # pre-make bit masks to speed up slicing and dicing
    BIT_LENGTH = 1280
    bits = [((1 << (i + 1)) - 1) for i in range(BIT_LENGTH)]

    def __init__(self, value=0):
        self.__value = value

    def __getitem__(self, index):
        """
        Get a single bit, 0 indexed

        :param index: Index of the bit to retrieve
        """
        if isinstance(index, slice):
            return self.__getslice__(index)
        return (self.__value >> index) & 1

    def __setitem__(self, index, value):
        """
        Set a single bit, 0 indexed

        :param index: Bit to set
        :param value: Value to set (will be masked to a single bit)
        """
        if isinstance(index, slice):
            return self.__setslice__(index, value)
        value = (value & 1) << index
        mask = ~(1 << index)
        self.__value = (self.__value & mask) | value

    def __getslice__(self, start_end):
        """
        Get a bit start_end, 0 indexed, not including the end index, exactly
        like a python list, so a[0:8] gives 8 bits in total... 0-7.
        Bit ranges are shifted down

        :param start: Start index
        :param end: End index
        :returns: integer masked to length bits.
        """
        start, end = start_end.start, start_end.stop
        # mask = 2 ** (end - start + 1)
        # But we want to allow x[:-1] e.g.
        if end > self.BIT_LENGTH:
            end = self.BIT_LENGTH
        elif end < 0:
            end += self.BIT_LENGTH

        if start < 0:
            start += self.BIT_LENGTH
        mask = self.bits[end - start - 1]
        return (self.__value >> start) & mask

    def __setslice__(self, start_end, value):
        """
        Set a bit start_end, 0 indexed, not including the end index, exactly
        like a python list, so a[0:8] sets bits 0 - 7.

        :param start: Start index
        :param end: End index
        :param value: Value to set (will be masked to correct number of bits)
        """
        start, end = start_end.start, start_end.stop
        if end < 0:
            end += self.BIT_LENGTH

        mask = self.bits[end - start - 1]
        value = (value & mask) << start
        mask <<= start
        self.__value = (self.__value & ~mask) | value
        return (self.__value >> start) & mask

    def __int__(self):
        """
        Cast ourselves to an integer value
        """
        return int(self.__value)

    def __long__(self):
        """
        Cast ourselves as a long integer value
        """
        return self.__value

    def __or__(self, other):
        """
        Bitwise or
        """
        return self.__value | other

    def __ror__(self, other):
        """
        Bitwise or where we're on the right hand side
        """
        return self.__value | other

    def __and__(self, other):
        """
        Bitwise and
        """
        return self.__value & other

    def __rand__(self, other):
        """
        Bitwise and where we're on the right hand side
        """
        return self.__value & other

    def __add__(self, other):
        """
        Add ourselves to another numeric type object
        """
        return self.__value + other

    def __radd__(self, other):
        """
        Add ourselves to another numeric type object
        """
        return self.__value + other

    def __rsub__(self, other):
        """
        Subtract ourselves from another numeric type object
        """
        return other - self.__value

    def __mul__(self, other):
        """
        Multiply ourselves with another numeric object
        """
        return other * self.__value

    def __rmul__(self, other):
        """
        Multiply ourselves with another numeric object
        """
        return other * self.__value

    def __truediv__(self, other):
        """
        Divide ourselves with another numeric object
        """
        return self.__value / other

    def __rdiv__(self, other):
        """
        Divide another numeric object with ourselves
        """
        return other / self.__value

    def __str__(self):
        """
        Return hex representation
        """
        return "{0}".format(hex(self.__value))

    def __repr__(self):
        """
        Return our representation
        """
        return "<BitField: {}>".format(self.__str__())

    def as_words(self, nWords, wordLen=16, offset=0):
        """
        Return this as a series of 16 bit values

        :param nWords: Return this many words
        :param wordLen: Length of items in bits
        :param offset: Start at this bit offset into the current bitfield
        :return: List of words of `wordLen` bits
        """
        return list(self.as_words(nWords, wordLen, offset))

    def as_words_generator(self, nWords, wordLen=16, offset=0):
        """
        Generator to return this as a series of `wordLen` bit values

        :param nWords: Return this many words
        :param wordLen: Length of items in bits
        :param offset: Start at this bit offset into the current bitfield
        :return: Generator of words of `wordLen` bits
        """
        return (self[o:o + wordLen] for o in range(offset, offset + (nWords * wordLen), wordLen))

    def from_word_set(self, words, wordLen=16, offset=0):
        """
        Extend the bit field from a word bucket

        :param words: a iterable set of 16 bit values
        :param wordLen: Length of items in bits
        :param offset: Start at this bit offset into the current bitfield
        """
        for w, s in zip(words, range(offset, offset + len(words) * wordLen, wordLen)):
            self[s:s + wordLen] = w
