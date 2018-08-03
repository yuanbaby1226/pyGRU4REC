import torch


def get_recall(indices, targets):
    """ Calculates the recall score for the given predictions and targets

    Args:
        indices (Bxk): torch.LongTensor. top-k indices predicted by the model.
        targets (B): torch.LongTensor. actual target indices.

    Returns:
        recall (float): the recall score
    """
    targets = targets.view(-1, 1).expand_as(indices)  # (Bxk)
    hits = (targets == indices).nonzero()
    if len(hits) == 0: return 0
    n_hits = (targets == indices).nonzero()[:, :-1].size(0)
    recall = n_hits / targets.size(0)
    
    return recall

def get_mrr(indices, targets):
    """ Calculates the MRR score for the given predictions and targets

    Args:
        indices (Bxk): torch.LongTensor. top-k indices predicted by the model.
        targets (B): torch.LongTensor. actual target indices.

    Returns:
        mrr (float): the mrr score
    """
    targets = targets.view(-1,1).expand_as(indices)
    # ranks of the targets, if it appears in your indices
    hits = (targets == indices).nonzero()
    if len(hits) == 0: return 0
    ranks = hits[:, -1] + 1
    ranks = ranks.float()
    rranks = torch.reciprocal(ranks)  # reciprocal ranks
    mrr = torch.sum(rranks).data / targets.size(0)
    
    return mrr

# def getZipper(logits,k=5):
#     #Args:
#     #   logits(B, C): torch.LongTensor.The predicted logit for the next items.
#     #Return:
#     #   zipper (string) : the item zipper
#     scores, indices = torch.topk(logits, k, -1)

def evaluate(logits, targets, k=20):
    """ Evaluates the model using Recall@K, MRR@K scores.

    Args:
        logits (B,C): torch.LongTensor. The predicted logit for the next items.
        targets (B): torch.LongTensor. actual target indices.

    Returns:
        recall (float): the recall score
        mrr (float): the mrr score
    """
    _, indices = torch.topk(logits, k, -1)
    recall = get_recall(indices, targets)
    mrr = get_mrr(indices, targets)

    return recall, mrr
