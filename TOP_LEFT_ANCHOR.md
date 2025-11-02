# Top-Left Corner Anchor Approach

## New Strategy

Instead of padding around the detected box, we now:
1. **Use the top-left corner (x1, y1) as an anchor point**
2. **Expand width and height by 50% from that anchor**
3. **Create a predictable, consistent anonymization box**

## Why This Works Better

### Old Approach (Padding):
- Added padding on all sides
- Unpredictable shifts depending on detection accuracy
- Hard to tune for consistent coverage

### New Approach (Top-Left Anchor):
- Anchored to top-left corner
- Expands only right and down
- Predictable and consistent
- Easier to adjust

## Visual Comparison

### Old Approach (Padding):
```
Original Detection:
    [====]
    
With Padding (unpredictable):
  [========]  or  [======]  or  [=======]
  (depends on padding values)
```

### New Approach (Top-Left Anchor):
```
Original Detection:
(x1,y1)→ [====]
         
Expanded 50% from top-left:
(x1,y1)→ [=======]
         ↓       ↓
         width*1.5
         height*1.5
```

## Code Logic

```python
# Start from top-left corner
x1_final = x1  # Anchor point
y1_final = y1  # Anchor point

# Expand width and height by 50%
expanded_width = width * 1.5
expanded_height = height * 1.5

# Calculate bottom-right corner
x2_final = x1_final + expanded_width
y2_final = y1_final + expanded_height
```

## Example

### Original Detection:
```
x1=100, y1=200, x2=300, y2=250
width=200, height=50
```

### Expanded from Top-Left:
```
x1_final = 100 (anchor)
y1_final = 200 (anchor)

expanded_width = 200 * 1.5 = 300
expanded_height = 50 * 1.5 = 75

x2_final = 100 + 300 = 400
y2_final = 200 + 75 = 275

Final box: (100, 200, 400, 275)
Size: 300x75
```

## Expected Logs

```
✅ License plate accepted: 200x50, aspect=4.00, conf=0.85
  → Expanded from top-left: (100, 200, 400, 275), size: 300x75 (original: 200x50)
Anonymized plate 1 at (100, 200, 400, 275) size: 300x75 with #FFFF00
```

## Adjusting Expansion

If 50% expansion is not enough:

```python
# For 75% expansion (more coverage):
expanded_width = int(width * 1.75)
expanded_height = int(height * 1.75)

# For 100% expansion (double size):
expanded_width = int(width * 2.0)
expanded_height = int(height * 2.0)
```

If 50% is too much:

```python
# For 30% expansion:
expanded_width = int(width * 1.3)
expanded_height = int(height * 1.3)
```

## Benefits

✅ **Predictable** - Always anchored to top-left  
✅ **Consistent** - Same expansion ratio for all plates  
✅ **Simple** - Easy to understand and adjust  
✅ **Effective** - 50% expansion should cover full plate  
✅ **Directional** - Expands right and down from anchor  

## Testing

```bash
# Restart backend
python main.py

# Upload images with license plates
# The yellow box should:
# 1. Start at the detected top-left corner
# 2. Expand 50% larger in width and height
# 3. Cover the entire plate consistently
```

## Summary

✅ **Anchored** to top-left corner (x1, y1)  
✅ **Expanded** by 50% in width and height  
✅ **Predictable** coverage from anchor point  
✅ **Adjustable** expansion multiplier  

This approach should provide consistent, full coverage of all license plates! 🎯

