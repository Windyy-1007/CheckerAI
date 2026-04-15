"""Feature extraction from board string representation."""
import numpy as np


def extract_features(bstr):
    """Extract a feature vector from a 64-char board string.

    Features (32 total):
      0: white piece count
      1: black piece count
      2: white king count
      3: black king count
      4: material advantage (white - black, counting kings as 2)
      5: white back-row pieces (row 7)
      6: black back-row pieces (row 0)
      7: white center control (rows 3-4, cols 2-5)
      8: black center control (rows 3-4, cols 2-5)
      9-12: white pieces per quadrant
      13-16: black pieces per quadrant
      17: white advancement score (how far forward pieces are)
      18: black advancement score
      19: total pieces on board
      20-23: white king positions per quadrant
      24-27: black king positions per quadrant
      28: white mobility proxy (non-edge pieces)
      29: black mobility proxy
      30: piece ratio (white / total)
      31: king ratio advantage
    """
    features = np.zeros(32, dtype=np.float32)

    w_count = 0
    b_count = 0
    wk_count = 0
    bk_count = 0
    w_back = 0
    b_back = 0
    w_center = 0
    b_center = 0
    w_quad = [0, 0, 0, 0]
    b_quad = [0, 0, 0, 0]
    wk_quad = [0, 0, 0, 0]
    bk_quad = [0, 0, 0, 0]
    w_advance = 0.0
    b_advance = 0.0
    w_non_edge = 0
    b_non_edge = 0

    for i in range(64):
        row = i // 8
        col = i % 8
        ch = bstr[i]
        if ch == '0':
            continue

        # Quadrant index
        qr = 0 if row < 4 else 1
        qc = 0 if col < 4 else 1
        quad = qr * 2 + qc

        is_center = (3 <= row <= 4) and (2 <= col <= 5)
        is_edge = (row == 0 or row == 7 or col == 0 or col == 7)

        if ch == 'w':
            w_count += 1
            w_quad[quad] += 1
            w_advance += (7 - row) / 7.0
            if is_center:
                w_center += 1
            if row == 7:
                w_back += 1
            if not is_edge:
                w_non_edge += 1
        elif ch == 'W':
            w_count += 1
            wk_count += 1
            wk_quad[quad] += 1
            w_quad[quad] += 1
            if is_center:
                w_center += 1
            if not is_edge:
                w_non_edge += 1
        elif ch == 'b':
            b_count += 1
            b_quad[quad] += 1
            b_advance += row / 7.0
            if is_center:
                b_center += 1
            if row == 0:
                b_back += 1
            if not is_edge:
                b_non_edge += 1
        elif ch == 'B':
            b_count += 1
            bk_count += 1
            bk_quad[quad] += 1
            b_quad[quad] += 1
            if is_center:
                b_center += 1
            if not is_edge:
                b_non_edge += 1

    total = w_count + b_count
    w_material = w_count + wk_count  # kings counted twice (once in w_count, once extra)
    b_material = b_count + bk_count

    features[0] = w_count / 12.0
    features[1] = b_count / 12.0
    features[2] = wk_count / 12.0
    features[3] = bk_count / 12.0
    features[4] = (w_material - b_material) / 24.0
    features[5] = w_back / 4.0
    features[6] = b_back / 4.0
    features[7] = w_center / 8.0
    features[8] = b_center / 8.0
    features[9:13] = [q / 6.0 for q in w_quad]
    features[13:17] = [q / 6.0 for q in b_quad]
    features[17] = w_advance / 12.0 if w_count > 0 else 0
    features[18] = b_advance / 12.0 if b_count > 0 else 0
    features[19] = total / 24.0
    features[20:24] = [q / 3.0 for q in wk_quad]
    features[24:28] = [q / 3.0 for q in bk_quad]
    features[28] = w_non_edge / 12.0
    features[29] = b_non_edge / 12.0
    features[30] = (w_count / total) if total > 0 else 0.5
    features[31] = (wk_count - bk_count) / 12.0

    return features
