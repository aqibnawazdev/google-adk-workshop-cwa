# Instructor Pre-Workshop Checklist

## 7 Days Before Workshop

- [ ] Send participants setup instructions with 00-setup-verification.ipynb
- [ ] Include 48-hour verification deadline in communication
- [ ] Set up email folder/label for confirmation screenshots

## 48 Hours Before Workshop

Participants should be emailing confirmation screenshots.

### Tracking Confirmations

| Participant | Email Received | Screenshot Valid | Confirmed |
|-------------|----------------|------------------|-----------|
| [Name 1] | [ ] | [ ] | [ ] |
| [Name 2] | [ ] | [ ] | [ ] |

### Valid Screenshot Criteria

- Shows "READY FOR WORKSHOP" message
- Shows all 4 checks passed (PASS)
- Timestamp visible in screenshot (recent)

### Responding to Confirmations

**If valid:**
> Hi [Name],
>
> Your environment is verified and ready for the workshop!
> See you on [date].
>
> If you have any questions before then, just reply to this email.

**If issues found:**
> Hi [Name],
>
> I noticed [issue] in your verification screenshot.
>
> Please try: [specific fix from TROUBLESHOOTING.md]
>
> If you're still stuck, let's schedule a 15-minute call before the workshop.

## Day of Workshop

- [ ] Note which participants haven't confirmed (may need setup help)
- [ ] Have TROUBLESHOOTING.md open for quick reference
- [ ] First 5 minutes: Quick re-verification for anyone with issues

## Common Issues to Watch For

1. **API key expired** - Keys can expire; ask them to regenerate
2. **Wrong Python version** - Must be 3.11+
3. **ADK version mismatch** - Must be exactly 1.23.0
4. **Colab runtime reset** - Remind them to re-run setup cells
