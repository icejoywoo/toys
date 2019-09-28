#!/usr/bin/env python2.7
# encoding: utf-8

"""
    @brief: https://leetcode.com/problems/reverse-nodes-in-k-group/
    @author: icejoywoo
    @date: 2019-09-28
"""
# helper function to convert python list to ListNode
def list_node(l):
    if l:
        return ListNode(l[0], list_node(l[1:]))
    else:
        return None


# Definition for singly-linked list.
class ListNode(object):

    def __init__(self, x, next=None):
        self.val = x
        self.next = next

    def _to_list(self):
        p = self
        r = []
        while p:
            r.append(p.val)
            p = p.next
        return r

    def __repr__(self):
        return 'ListNode{val: %r, next: %r}' % (self.val, self.next._to_list() if self.next else None)


# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution(object):
    def reverseList(self, head):
        """
        :type head: ListNode
        :rtype: ListNode
        """
        prev, cur = None, head
        while cur:
            cur.next, prev, cur = prev, cur, cur.next
        return prev

    def reverseKGroup1(self, head, k):
        """
        :type head: ListNode
        :type k: int
        :rtype: ListNode
        """

        if head is None:
            return None

        pre_tail, h, p, c = None, head, None, head
        l = 0
        r = None

        while c:
            p, c = c, c.next
            l += 1

            if l == k:
                p.next = None
                new_h = self.reverseList(h)
                if r is None:
                    r = new_h

                if pre_tail:
                    pre_tail.next = new_h
                pre_tail = h

                h.next = c
                p, h = h, c
                l = 0

        if r is None:
            r = head

        return r

    def reverseKGroup(self, head, k):
        """
        :type head: ListNode
        :type k: int
        :rtype: ListNode
        """
        dummy = ListNode(None)
        prev, prev.next = dummy, head
        c = head
        l = 0

        while c:
            l += 1
            c = c.next

            if l == k:
                a, b = prev, prev.next
                while l > 0:
                    b.next, a, b = a, b, b.next
                    l -= 1

                prev.next.next = b
                prev.next, prev = a, prev.next

        return dummy.next


if __name__ == '__main__':
    s = Solution()
    print s.reverseKGroup(list_node([]), 3)
    print s.reverseKGroup(list_node([1]), 3)
    print s.reverseKGroup(list_node([1, 2, 3, 4, 5]), 1)
    print s.reverseKGroup(list_node([1, 2, 3, 4, 5]), 2)  # 2 1 4 3 5
    print s.reverseKGroup(list_node([1, 2, 3, 4, 5]), 3)  # 2 1 4 3
