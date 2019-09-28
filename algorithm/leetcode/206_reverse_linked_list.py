# encoding: utf-8
# https://leetcode.com/problems/reverse-linked-list/

# helper function to convert python list to ListNode
def list_node(l):
    if l:
        nodes = [ListNode(i) for i in l]
        head = nodes[0]
        p = head
        for i in nodes[1:]:
            p.next = i
            p = i
        return head
    else:
        return None

# Definition for singly-linked list.
class ListNode(object):

    def __init__(self, x):
        self.val = x
        self.next = None

    def _to_list(self):
        p = self
        r = []
        while p:
            r.append(p.val)
            p = p.next
        return r

    def __repr__(self):
        return 'ListNode{val: %r, next: %r}' % (self.val, self.next._to_list() if self.next else None)


class Solution(object):
    def reverseList1(self, head):
        """
        :type head: ListNode
        :rtype: ListNode
        """
        # empty list
        if head is None:
            return head

        p = None
        q = head
        while q:
            # q.next, p, q = p, q, q.next
            # 一句简写貌似是和顺序有一定关系的
            t = q.next
            q.next = p
            p, q = q, t

        return p

    def reverseList(self, head):
        """
        :type head: ListNode
        :rtype: ListNode
        """
        prev, cur = None, head
        while cur:
            cur.next, prev, cur = prev, cur, cur.next
        return prev


if __name__ == '__main__':
    s = Solution()
    print s.reverseList(list_node([]))
    print s.reverseList(list_node([1]))
    print s.reverseList(list_node([1, 2, 3, 4, 5]))
