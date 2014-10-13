""" 
This is a project for Algorithmic Thinking, week 4
"""

def build_scoring_matrix(alphabet, diag_score, off_diag_score, dash_score):
    """ 
    The function returns a dictionary of dictionaries whose entries are indexed by pairs of characters in 
    alphabet plus '-'. The score for any entry indexed by one or more dashes is dash_score. The score for the 
    remaining diagonal entries is diag_score. Finally, the score for the remaining off-diagonal entries is off_diag_score.
    """
    enriched_alphabet = list(alphabet)
    enriched_alphabet.append('-')
    result = dict()
    for first_letter in enriched_alphabet:
        pair = dict()
        for second_letter in enriched_alphabet:
            if first_letter == '-' or second_letter == '-':
                pair[second_letter] = dash_score
            elif first_letter != second_letter:
                pair[second_letter] = off_diag_score
            else:
                pair[second_letter] = diag_score
            result[first_letter] = pair
    return result

def compute_alignment_matrix(seq_x, seq_y, scoring_matrix, global_flag):
    """
    If global_flag is False then negative values in alignment matrix should be replaced with zero.
    """
    len_x = len(seq_x)
    len_y = len(seq_y)
    result = list()
    result.append(list([0]))
    for index_x in range(1, len_x + 1):
        value = result[index_x - 1][0] + scoring_matrix[seq_x[index_x - 1]]['-']
        if value < 0 and not global_flag:
            value = 0
        result.append(list([value]))
    for index_y in range(1, len_y + 1):
        value = result[0][index_y - 1] + scoring_matrix['-'][seq_y[index_y - 1]]
        if value < 0 and not global_flag:
            value = 0
        result[0].append(value)  
        
    for index_x in range(1, len_x + 1):
        for index_y in range(1, len_y + 1):
            value = max(result[index_x - 1][index_y - 1] + scoring_matrix[seq_x[index_x - 1]][seq_y[index_y - 1]],
                        result[index_x - 1][index_y] + scoring_matrix[seq_x[index_x - 1]]['-'],
                        result[index_x][index_y - 1] + scoring_matrix['-'][seq_y[index_y - 1]])
            if value < 0 and not global_flag:
                value = 0
            result[index_x].append(value)
    return result

def compute_global_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
    """
    This function computes a global alignment of seq_x and seq_y using the global alignment matrix alignment_matrix.
    Returns a tuple of the form (score, align_x, align_y).
    """
    index_x = len(seq_x)
    index_y = len(seq_y)
    
    alignment_x = ''
    alignment_y = ''
    
    while index_x != 0 and index_y != 0:
        if alignment_matrix[index_x][index_y] == alignment_matrix[index_x - 1][index_y - 1] + scoring_matrix[seq_x[index_x - 1]][seq_y[index_y - 1]]:
            alignment_x = seq_x[index_x - 1] + alignment_x
            alignment_y = seq_y[index_y - 1] + alignment_y
            index_x -= 1
            index_y -= 1
        elif alignment_matrix[index_x][index_y] == alignment_matrix[index_x - 1][index_y] + scoring_matrix[seq_x[index_x - 1]]['-']:
            alignment_x = seq_x[index_x - 1] + alignment_x
            alignment_y = '-' + alignment_y
            index_x -= 1
        else:
            alignment_x = '-' + alignment_x
            alignment_y = seq_y[index_y - 1] + alignment_y
            index_y -= 1
    while index_x != 0:
        alignment_x = seq_x[index_x - 1] + alignment_x
        alignment_y = '-' + alignment_y
        index_x -= 1    
    while index_y != 0:
        alignment_x = '-' + alignment_x
        alignment_y = seq_y[index_y - 1] + alignment_y
        index_y -= 1        
    return (compute_score(alignment_x, alignment_y, scoring_matrix), alignment_x, alignment_y)

def compute_score(alignment_x, alignment_y, scoring_matrix):
    """
    Computes score between two alignments using scoring matrix.
    """
    result = 0
    if len(alignment_x) != len(alignment_y):
        return result
    for index in range(len(alignment_x)):
        result += scoring_matrix[alignment_x[index]][alignment_y[index]]
    return result

def compute_local_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
    """
    Computes a local alignment of seq_x and seq_y using the local alignment matrix alignment_matrix. 
    """
    
    #finding max in alignment matrix
    
    max_x = 0
    max_y = 0
    max_value = alignment_matrix[0][0]
    for index_x in range(len(alignment_matrix)):
        for index_y in range(len(alignment_matrix[0])):
            if alignment_matrix[index_x][index_y] > max_value:
                max_x = index_x
                max_y = index_y
                max_value = alignment_matrix[index_x][index_y]
    
    index_x = max_x
    index_y = max_y
    
    alignment_x = ''
    alignment_y = ''
    
    while index_x != 0 and index_y != 0:
        if alignment_matrix[index_x][index_y] == 0:
            return (max_value, alignment_x, alignment_y)
        if alignment_matrix[index_x][index_y] == alignment_matrix[index_x - 1][index_y - 1] + scoring_matrix[seq_x[index_x - 1]][seq_y[index_y - 1]]:
            alignment_x = seq_x[index_x - 1] + alignment_x
            alignment_y = seq_y[index_y - 1] + alignment_y
            index_x -= 1
            index_y -= 1
        elif alignment_matrix[index_x][index_y] == alignment_matrix[index_x - 1][index_y] + scoring_matrix[seq_x[index_x - 1]]['-']:
            alignment_x = seq_x[index_x - 1] + alignment_x
            alignment_y = '-' + alignment_y
            index_x -= 1
        else:
            alignment_x = '-' + alignment_x
            alignment_y = seq_y[index_y - 1] + alignment_y
            index_y -= 1
    while index_x != 0:
        if alignment_matrix[index_x][index_y] == 0:
            return (max_value, alignment_x, alignment_y)
        alignment_x = seq_x[index_x - 1] + alignment_x
        alignment_y = '-' + alignment_y
        index_x -= 1    
    while index_y != 0:
        if alignment_matrix[index_x][index_y] == 0:
            return (max_value, alignment_x, alignment_y)
        alignment_x = '-' + alignment_x
        alignment_y = seq_y[index_y - 1] + alignment_y
        index_y -= 1            
    return (max_value, alignment_x, alignment_y)
