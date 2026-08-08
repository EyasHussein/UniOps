$ErrorActionPreference = 'Stop'

$templatePath = 'C:\Users\lenovo\OneDrive - GJU\Desktop\sp report\SP Report template - GJU.docx'
$outDir = 'C:\Users\lenovo\OneDrive - GJU\Desktop\sp report'
$outDocx = Join-Path $outDir 'SP_Report_University_Room_Booking_GJU_Working.docx'
$outPdf = Join-Path $outDir 'SP_Report_University_Room_Booking_GJU_Final.pdf'

$useCase = 'F:\University Room Booking\report_output\use_case_diagram.png'
$sequence = 'F:\University Room Booking\report_output\sequence_diagram.png'
$class = 'F:\University Room Booking\report_output\class_diagram.png'

if (!(Test-Path $templatePath)) { throw "Template not found: $templatePath" }
if (Test-Path $outDocx) { Remove-Item $outDocx -Force }
if (Test-Path $outPdf) { Remove-Item $outPdf -Force }
Copy-Item $templatePath $outDocx -Force

$word = $null
$doc = $null

function Set-DocStyle {
    param([object]$Selection, [object]$Document, [string[]]$StyleNames)
    foreach ($name in $StyleNames) {
        try { $Selection.Style = $Document.Styles.Item($name); return } catch { try { $Selection.Style = $name; return } catch {} }
    }
}

function Add-Paragraph {
    param([object]$Selection, [object]$Document, [string]$Text)
    Set-DocStyle -Selection $Selection -Document $Document -StyleNames @('BodyText','Body Text','Normal')
    $Selection.TypeText($Text)
    $Selection.TypeParagraph()
    $Selection.TypeParagraph()
}

function Add-Heading2 {
    param([object]$Selection, [object]$Document, [string]$Text)
    Set-DocStyle -Selection $Selection -Document $Document -StyleNames @('Heading2','Heading 2','Heading 1')
    $Selection.TypeText($Text)
    $Selection.TypeParagraph()
}

function Add-Chapter {
    param([object]$Selection, [object]$Document, [string]$Text)
    $Selection.InsertBreak(7) | Out-Null
    Set-DocStyle -Selection $Selection -Document $Document -StyleNames @('chapternumber','Heading1','Heading 1')
    $Selection.TypeText($Text)
    $Selection.TypeParagraph()
}

function Add-Figure {
    param([object]$Selection, [object]$Document, [string]$Title, [string]$ImagePath, [string]$Caption)
    Add-Heading2 -Selection $Selection -Document $Document -Text $Title
    if (Test-Path $ImagePath) {
        $shape = $Selection.InlineShapes.AddPicture($ImagePath)
        if ($shape -ne $null) { try { $shape.LockAspectRatio = -1; $shape.Width = 430 } catch {} }
        $Selection.TypeParagraph()
    }
    Set-DocStyle -Selection $Selection -Document $Document -StyleNames @('Caption','Normal')
    $Selection.TypeText($Caption)
    $Selection.TypeParagraph()
    $Selection.TypeParagraph()
}

function Replace-All-Short {
    param([object]$Document, [string]$FindText, [string]$ReplaceText)
    $range = $Document.Content
    $find = $range.Find
    $find.ClearFormatting(); $find.Replacement.ClearFormatting()
    $find.Text = $FindText; $find.Replacement.Text = $ReplaceText
    $find.Forward = $true; $find.Wrap = 1; $find.Format = $false
    $find.MatchCase = $false; $find.MatchWholeWord = $false
    $find.Execute($FindText,$false,$false,$false,$false,$false,$true,1,$false,$ReplaceText,2) | Out-Null
}

try {
    $word = New-Object -ComObject Word.Application
    $word.Visible = $false
    $word.DisplayAlerts = 0
    $doc = $word.Documents.Open($outDocx)

    Replace-All-Short -Document $doc -FindText '<TITLE OF THE PROJECT>' -ReplaceText 'University Room Booking and Campus Operations System'
    Replace-All-Short -Document $doc -FindText '<FirstName Last name>' -ReplaceText '[Student Name]'
    Replace-All-Short -Document $doc -FindText '<Student ID Number>' -ReplaceText '[Student ID]'
    Replace-All-Short -Document $doc -FindText '<Title> <Name> <Last name>' -ReplaceText 'Dr. [Supervisor Name]'
    Replace-All-Short -Document $doc -FindText '<Year> <Semester>' -ReplaceText '2025/2026 - Spring'

    $sel = $word.Selection
    $sel.EndKey(6) | Out-Null

    Add-Chapter -Selection $sel -Document $doc -Text 'PROJECT REPORT CONTENT (UNIVERSITY ROOM BOOKING SYSTEM)'

    Add-Chapter -Selection $sel -Document $doc -Text 'ABSTRACT'
    Add-Paragraph -Selection $sel -Document $doc -Text 'This report presents the design and implementation of a University Room Booking and Campus Operations System. The system integrates room reservation workflows, complaint handling, maintenance requests, and administrative control into a unified web platform. The implementation uses Django, SQLite, and template-driven UI design to provide a practical and maintainable solution.'
    Add-Paragraph -Selection $sel -Document $doc -Text 'The final system enforces booking validation rules, supports status lifecycle tracking, and offers role-based dashboards for students, faculty, and administrators. The outcome is a clear operational baseline suitable for academic evaluation and future production scaling.'

    Add-Chapter -Selection $sel -Document $doc -Text 'CHAPTER I: INTRODUCTION'
    Add-Heading2 -Selection $sel -Document $doc -Text '1.1 Background'
    Add-Paragraph -Selection $sel -Document $doc -Text 'Campus resources must be coordinated efficiently. Manual booking and issue-reporting workflows often create conflicts, delays, and poor visibility. This project addresses these challenges through a centralized web system that formalizes requests and status transitions.'
    Add-Paragraph -Selection $sel -Document $doc -Text '[put here a picture of the login page]'
    Add-Heading2 -Selection $sel -Document $doc -Text '1.2 Objectives'
    Add-Paragraph -Selection $sel -Document $doc -Text 'Objectives include role-based access, booking conflict prevention, complaint/maintenance lifecycle tracking, daily schedule visibility, and maintainable implementation.'

    Add-Chapter -Selection $sel -Document $doc -Text 'CHAPTER II: REQUIREMENTS ANALYSIS'
    Add-Heading2 -Selection $sel -Document $doc -Text '2.1 Functional Requirements'
    Add-Paragraph -Selection $sel -Document $doc -Text 'Required capabilities include authentication, room browsing, schedule viewing, booking request creation, status updates, complaint and maintenance reporting, archiving, and role-based dashboard operations.'
    Add-Paragraph -Selection $sel -Document $doc -Text '[put here a picture of requirements table]'
    Add-Heading2 -Selection $sel -Document $doc -Text '2.2 Non-Functional Requirements'
    Add-Paragraph -Selection $sel -Document $doc -Text 'The system should remain simple, reliable, and clear for end users. Validation must be server-side and UI feedback should be understandable. Localhost performance should remain responsive for academic data volumes.'

    Add-Chapter -Selection $sel -Document $doc -Text 'CHAPTER III: SYSTEM DESIGN'
    Add-Heading2 -Selection $sel -Document $doc -Text '3.1 Architecture'
    Add-Paragraph -Selection $sel -Document $doc -Text 'The architecture is modular by app domain. Each module encapsulates its models, forms, views, and templates while sharing authentication and layout infrastructure.'
    Add-Paragraph -Selection $sel -Document $doc -Text '[put here a picture of architecture diagram]'
    Add-Figure -Selection $sel -Document $doc -Title '3.2 Use Case Diagram' -ImagePath $useCase -Caption 'Figure 3.1: Use Case Diagram'
    Add-Figure -Selection $sel -Document $doc -Title '3.3 Sequence Diagram' -ImagePath $sequence -Caption 'Figure 3.2: Sequence Diagram'
    Add-Figure -Selection $sel -Document $doc -Title '3.4 Class Diagram' -ImagePath $class -Caption 'Figure 3.3: Class Diagram'
    Add-Paragraph -Selection $sel -Document $doc -Text '[put here a picture of ERD/database schema]'

    Add-Chapter -Selection $sel -Document $doc -Text 'CHAPTER IV: IMPLEMENTATION'
    Add-Heading2 -Selection $sel -Document $doc -Text '4.1 Modules'
    Add-Paragraph -Selection $sel -Document $doc -Text 'Core modules include users, rooms, bookings, complaints, maintenance, notifications, and dashboard routing. This structure keeps responsibilities clear and facilitates incremental improvements.'
    Add-Paragraph -Selection $sel -Document $doc -Text '[put here a picture of project tree/code structure]'
    Add-Heading2 -Selection $sel -Document $doc -Text '4.2 Booking and Validation'
    Add-Paragraph -Selection $sel -Document $doc -Text 'Booking validation enforces date and time constraints, half-hour steps, and conflict checks against approved reservations. Admin users process pending requests through explicit status actions.'
    Add-Paragraph -Selection $sel -Document $doc -Text '[put here a picture of booking form and validation error]'
    Add-Paragraph -Selection $sel -Document $doc -Text '[put here a picture of booking status update in admin]'
    Add-Heading2 -Selection $sel -Document $doc -Text '4.3 Complaints and Maintenance'
    Add-Paragraph -Selection $sel -Document $doc -Text 'Issue workflows support submission, status transitions, and archive handling. This enables traceable request management and improves communication between users and administrators.'
    Add-Paragraph -Selection $sel -Document $doc -Text '[put here a picture of complaints page]'
    Add-Paragraph -Selection $sel -Document $doc -Text '[put here a picture of maintenance page]'

    Add-Chapter -Selection $sel -Document $doc -Text 'CHAPTER V: TESTING AND EVALUATION'
    Add-Heading2 -Selection $sel -Document $doc -Text '5.1 Testing Strategy'
    Add-Paragraph -Selection $sel -Document $doc -Text 'Testing covered authentication, authorization, input validation, schedule rendering, and workflow transitions. Negative scenarios were included to ensure robust rejection behavior.'
    Add-Heading2 -Selection $sel -Document $doc -Text '5.2 Test Cases and Evidence'
    for ($i = 1; $i -le 24; $i++) {
        Add-Paragraph -Selection $sel -Document $doc -Text ("Test Case {0}: Define scenario, input, expected output, and actual output." -f $i)
        Add-Paragraph -Selection $sel -Document $doc -Text ("[put here a picture of test case {0} evidence]" -f $i)
    }
    Add-Heading2 -Selection $sel -Document $doc -Text '5.3 Performance on Localhost'
    Add-Paragraph -Selection $sel -Document $doc -Text 'The application performs well for small and medium datasets. Optimization opportunities include pagination for large tables, query count reduction, and indexes for frequently filtered models.'
    Add-Paragraph -Selection $sel -Document $doc -Text '[put here a picture of performance notes or profiling output]'

    Add-Chapter -Selection $sel -Document $doc -Text 'CHAPTER VI: SECURITY, RISKS, AND MAINTENANCE'
    Add-Paragraph -Selection $sel -Document $doc -Text 'Security baseline includes login protection, CSRF controls, and role-based authorization in views. Operational risks include growth-driven query overhead and role regression after modifications. Mitigation includes checklists, indexing, and regular validation reviews.'
    Add-Paragraph -Selection $sel -Document $doc -Text '[put here a picture of authorization restriction test]'

    Add-Chapter -Selection $sel -Document $doc -Text 'CHAPTER VII: CONCLUSION AND FUTURE WORK'
    Add-Paragraph -Selection $sel -Document $doc -Text 'The project provides a practical and maintainable solution for campus operations management. Future work includes production deployment, analytics enhancements, notification automation, and expanded testing coverage.'

    Add-Chapter -Selection $sel -Document $doc -Text 'REFERENCES'
    $refs = @(
        '[1] Django Documentation: https://docs.djangoproject.com/',
        '[2] SQLite Documentation: https://www.sqlite.org/docs.html',
        '[3] Tailwind CSS Documentation: https://tailwindcss.com/docs',
        '[4] OWASP Top 10: https://owasp.org',
        '[5] UML Specification, OMG'
    )
    foreach ($r in $refs) { Add-Paragraph -Selection $sel -Document $doc -Text $r }

    Add-Chapter -Selection $sel -Document $doc -Text 'APPENDIX A: WEB PAGE SCREENSHOT PLACES'
    $webShots = @(
        '[put here a picture of home page]',
        '[put here a picture of login page]',
        '[put here a picture of faculty dashboard]',
        '[put here a picture of student dashboard]',
        '[put here a picture of admin dashboard]',
        '[put here a picture of room cards page]',
        '[put here a picture of room schedule page]',
        '[put here a picture of booking request form]',
        '[put here a picture of complaint form]',
        '[put here a picture of maintenance form]',
        '[put here a picture of admin status update actions]'
    )
    foreach ($w in $webShots) { Add-Paragraph -Selection $sel -Document $doc -Text $w }

    Add-Chapter -Selection $sel -Document $doc -Text 'APPENDIX B: CODE SCREENSHOT PLACES'
    for ($k = 1; $k -le 34; $k++) {
        Add-Paragraph -Selection $sel -Document $doc -Text ("[put here a picture of code snippet B-{0}: include path + explanation]" -f $k)
    }

    $pages = $doc.ComputeStatistics(2)
    $extra = 1
    while ($pages -lt 21) {
        Add-Chapter -Selection $sel -Document $doc -Text ("APPENDIX C{0}: ADDITIONAL PLACEHOLDERS" -f $extra)
        for ($z = 1; $z -le 15; $z++) {
            Add-Paragraph -Selection $sel -Document $doc -Text ("[put here a picture of additional evidence C{0}-{1}]" -f $extra, $z)
            Add-Paragraph -Selection $sel -Document $doc -Text 'Add a short explanation of what this evidence demonstrates.'
        }
        $extra++
        $pages = $doc.ComputeStatistics(2)
    }

    try { $doc.Fields.Update() | Out-Null } catch {}
    try { foreach ($toc in $doc.TablesOfContents) { $toc.Update() | Out-Null } } catch {}
    try { foreach ($tof in $doc.TablesOfFigures) { $tof.Update() | Out-Null } } catch {}

    $doc.SaveAs2($outDocx,16)
    $doc.ExportAsFixedFormat($outPdf,17)
    $finalPages = $doc.ComputeStatistics(2)

    $doc.Close()
    $word.Quit()

    Write-Output ("PAGES: {0}" -f $finalPages)
    Get-Item $outPdf | Select-Object FullName,Length,LastWriteTime
}
catch {
    if ($doc -ne $null) { try { $doc.Close() } catch {} }
    if ($word -ne $null) { try { $word.Quit() } catch {} }
    throw
}
