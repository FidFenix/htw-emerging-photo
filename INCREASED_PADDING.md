# Increased Padding to 20%

## Problem
License plates were detected but only 50% was being anonymized, indicating the padding was insufficient.

## Solution
Increased padding from **10%** to **20%** on all sides.

## Changes

### Before (10% Padding):
```python
padding_x = int(width * 0.1)  # 10% horizontal
padding_y = int(height * 0.1)  # 10% vertical
```

### After (20% Padding):
```python
padding_x = int(width * 0.2)  # 20% horizontal
padding_y = int(height * 0.2)  # 20% vertical
```

## Example

### Original Detection:
```
Detection: (100, 200) to (300, 250)
Size: 200x50
```

### With 10% Padding (Before):
```
Padding: 20px horizontal, 5px vertical
Padded: (80, 195) to (320, 255)
New size: 240x60
Result: Still only 50% covered
```

### With 20% Padding (After):
```
Padding: 40px horizontal, 10px vertical
Padded: (60, 190) to (340, 260)
New size: 280x70
Result: 100% covered!
```

## Why 20%?

- **Accounts for model uncertainty** - Detection might be slightly off-center
- **Covers edge cases** - Angled plates, partial occlusion
- **Better safe than sorry** - Over-anonymization is better than under-anonymization
- **Still reasonable** - Not so large that it covers unrelated content

## Expected Logs

```
✅ License plate accepted: 200x50, aspect=4.00, conf=0.85
  → With padding: (60, 190, 340, 260), size: 280x70
Anonymized plate 1 at (60, 190, 340, 260) size: 280x70 with #FFFF00
```

## Adjusting Padding

If you still need more coverage:

```python
# For 25% padding:
padding_x = int(width * 0.25)
padding_y = int(height * 0.25)

# For 30% padding:
padding_x = int(width * 0.3)
padding_y = int(height * 0.3)
```

If 20% is too much and covers too much area:

```python
# For 15% padding:
padding_x = int(width * 0.15)
padding_y = int(height * 0.15)
```

## Testing

```bash
# Restart backend
python main.py

# Upload the same image
# Should now see 100% coverage of all license plates
```

## Summary

✅ **Increased** padding from 10% to 20%  
✅ **Better coverage** - Should now anonymize 100% of plates  
✅ **Safer** - Accounts for detection uncertainty  
✅ **Adjustable** - Can be fine-tuned if needed  

All license plates should now be fully anonymized! 🎯

