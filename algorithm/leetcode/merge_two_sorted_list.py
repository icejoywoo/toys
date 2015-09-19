#!/bin/env python
# encoding: utf-8

__author__ = 'icejoywoo'

# Definition for singly-linked list.
class ListNode(object):
    def __init__(self, x):
        self.val = x
        self.next = None

    def __repr__(self):
        return '%d, %r' % (self.val, self.next)

class Solution(object):
    def mergeTwoLists(self, l1, l2):
        """
        :type l1: ListNode
        :type l2: ListNode
        :rtype: ListNode
        """
        def closure():
            result_head = [None]
            result = [None]
            def _wrapper(x):
                if result[0]:
                    result[0].next = ListNode(x)
                    result[0] = result[0].next
                else:
                    result[0] = ListNode(x)
                    result_head[0] = result[0]
                return result_head[0]
            return _wrapper

        append = closure()

        result = None

        while l1 and l2:
            if l1.val < l2.val:
                result = append(l1.val)
                l1 = l1.next
            else:
                result = append(l2.val)
                l2 = l2.next
        while l1:
            result = append(l1.val)
            l1 = l1.next

        while l2:
            result = append(l2.val)
            l2 = l2.next

        return result


if __name__ == '__main__':
    s = Solution()
    print s.mergeTwoLists(None, None)
    print s.mergeTwoLists(None, ListNode(1))
    a = ListNode(1)
    a.next = ListNode(2)
    a.next.next = ListNode(4)
    print s.mergeTwoLists(None, a)
