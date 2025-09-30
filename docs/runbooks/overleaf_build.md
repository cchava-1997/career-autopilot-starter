# Overleaf Build Runbook

## Overview
This runbook covers troubleshooting Overleaf PDF builds and common issues.

## Prerequisites
- Overleaf API key configured
- Project IDs set for each track (PO/PM/TPM)
- LaTeX environment installed (BasicTeX or MacTeX)

## Common Issues

### 1. Build Timeout
**Symptoms**: PDF build fails with timeout error
**Solutions**:
- Check Overleaf project size and complexity
- Verify LaTeX compilation time
- Consider breaking down large documents

### 2. Missing Dependencies
**Symptoms**: LaTeX compilation errors
**Solutions**:
- Ensure all required packages are included
- Check for missing fonts or graphics
- Verify template compatibility

### 3. API Authentication Issues
**Symptoms**: 401/403 errors from Overleaf API
**Solutions**:
- Verify API key is correct
- Check project permissions
- Ensure project IDs are valid

### 4. File Path Issues
**Symptoms**: Cannot find template files
**Solutions**:
- Verify template paths in configuration
- Check file permissions
- Ensure relative paths are correct

## Troubleshooting Steps

1. **Check Logs**
   ```bash
   tail -f apps/backend/logs/app.log.jsonl | grep overleaf
   ```

2. **Test API Connection**
   ```bash
   curl -H "Authorization: Bearer $OVERLEAF_API_KEY" \
        https://www.overleaf.com/api/v1/projects
   ```

3. **Verify Project Access**
   - Open project URL in browser
   - Check if project is accessible
   - Verify project settings

4. **Test LaTeX Compilation**
   ```bash
   pdflatex data/templates/resume_template.tex
   ```

## Recovery Procedures

### Failed Build Recovery
1. Check error logs for specific issues
2. Verify template file integrity
3. Test with minimal template
4. Rebuild with clean state

### API Rate Limit Handling
1. Implement exponential backoff
2. Cache successful builds
3. Queue build requests
4. Monitor API usage

## Monitoring

### Key Metrics
- Build success rate
- Average build time
- API error rate
- Template usage frequency

### Alerts
- Build failure rate > 10%
- Average build time > 2 minutes
- API error rate > 5%
- Template compilation errors
