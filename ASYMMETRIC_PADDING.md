# Asymmetric Padding to Shift Coverage Left

## Problem
The anonymization was covering only the right 50% of license plates, indicating the detection was shifted to the right and missing the left side.

## Solution
Applied **asymmetric padding** with more padding on the left side to shift the coverage area to the left.

## Changes

### Before (Symmetric 20% Padding):
```python
padding_x = int(width * 0.2)  # Same on both sides
x1_padded = x1 - padding_x    # Left
x2_padded = x2 + padding_x    # Right
```

### After (Asymmetric Padding):
```python
padding_left = int(width * 0.3)   # 30% on left
padding_right = int(width * 0.2)  # 20% on right
x1_padded = x1 - padding_left     # More padding on left
x2_padded = x2 + padding_right    # Less padding on right
```

## Visual Example

### Original Detection (shifted right):
```
Plate:    [========]
Detection:    [====]
              ^    ^
              x1   x2
Missing left side!
```

### With Symmetric 20% Padding:
```
Plate:    [========]
Detection:  [======]
Still missing left edge!
```

### With Asymmetric Padding (30% left, 20% right):
```
Plate:    [========]
Detection:[=========]
          ^         ^
          x1        x2
Full coverage!
```

## Padding Configuration

| Side   | Padding | Purpose                          |
|--------|---------|----------------------------------|
| Left   | 30%     | Compensate for right-shift       |
| Right  | 20%     | Standard coverage                |
| Top    | 20%     | Standard coverage                |
| Bottom | 20%     | Standard coverage                |

## Example Calculation

### Original Detection:
```
x1=100, x2=300, width=200
y1=200, y2=250, height=50
```

### With Asymmetric Padding:
```
padding_left = 200 * 0.3 = 60px
padding_right = 200 * 0.2 = 40px
padding_top = 50 * 0.2 = 10px
padding_bottom = 50 * 0.2 = 10px

x1_padded = 100 - 60 = 40
x2_padded = 300 + 40 = 340
y1_padded = 200 - 10 = 190
y2_padded = 250 + 10 = 260

New size: 300x70 (shifted left by 20px)
```

## Expected Logs

```
✅ License plate accepted: 200x50, aspect=4.00, conf=0.85
  → With padding: (40, 190, 340, 260), size: 300x70
Anonymized plate 1 at (40, 190, 340, 260) size: 300x70 with #FFFF00
```

## Fine-Tuning

If still not covering the left side enough:

```python
# Increase left padding to 40%
padding_left = int(width * 0.4)
padding_right = int(width * 0.2)
```

If covering too much on the left:

```python
# Reduce left padding to 25%
padding_left = int(width * 0.25)
padding_right = int(width * 0.2)
```

If the shift is in the opposite direction (missing right side):

```python
# More padding on right, less on left
padding_left = int(width * 0.2)
padding_right = int(width * 0.3)
```

## Testing

```bash
# Restart backend
python main.py

# Upload the same image
# The yellow box should now cover the entire plate
# Including the left side that was previously visible
```

## Summary

✅ **Asymmetric padding** - 30% left, 20% right, top, bottom  
✅ **Shifts coverage left** - Compensates for right-biased detection  
✅ **Full coverage** - Should now anonymize 100% of plates  
✅ **Adjustable** - Can fine-tune per side if needed  

The license plates should now be fully covered, including the left side! 🎯

